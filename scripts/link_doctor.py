# ? Project: Exiles Installer
# ? File: link_doctor.py
# ? Directory: scripts/
# ? Description: Audits and (optionally) auto-fixes links in src/apps.json: HTTP, GitHub assets, winget IDs.
# ? Created by: Watty
# ? Created on: 2025-09-30
# ? Last modified by: Watty
# ? Last modified on: 2025-09-30

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import requests

ROOT = Path(__file__).resolve().parents[1]
APPS_JSON = ROOT / "src" / "apps.json"
ARTIFACTS = ROOT / "artifacts"
TIMEOUT = 15

OK_HEAD = {200, 301, 302, 303, 307, 308}
OK_ANY = set(range(200, 400))

@dataclass
class Finding:
    app_id: str
    app_name: str
    source: str         # http|github|winget
    message: str
    old: Optional[str] = None
    new: Optional[str] = None
    note: Optional[str] = None
    fixed: bool = False

@dataclass
class Context:
    config: Dict[str, Any]
    findings: List[Finding] = field(default_factory=list)
    session: requests.Session = field(default_factory=requests.Session)
    dry_run: bool = True

def load_config(path: Path) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_config(path: Path, cfg: Dict[str, Any]):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)

def backup_config(path: Path) -> Path:
    ARTIFACTS.mkdir(exist_ok=True)
    ts = time.strftime("%Y%m%d-%H%M%S")
    backup = ARTIFACTS / f"apps.backup.{ts}.json"
    shutil.copy2(path, backup)
    return backup

def check_url(session: requests.Session, url: str) -> Tuple[bool, int, Optional[str], Optional[str]]:
    """
    Returns (ok, status_code, final_url, note)
    - HEAD first; fall back to GET (some sites 204/403/405 on HEAD)
    """
    try:
        r = session.head(url, timeout=TIMEOUT, allow_redirects=True)
        sc = r.status_code
        if sc in OK_HEAD:
            return True, sc, str(r.url), None
        # retry GET
        r = session.get(url, timeout=TIMEOUT, allow_redirects=True, stream=True)
        r.close()
        sc = r.status_code
        if sc in OK_ANY:
            return True, sc, str(r.url), "passed on GET"
        return False, sc, str(r.url), None
    except Exception as e:
        return False, -1, None, f"exception: {e}"

def run_text(cmd, timeout=25):
    """
    Run a command and return CompletedProcess with UTF-8-decoded text output.
    We force encoding to avoid cp1252 UnicodeDecodeError on some consoles.
    """
    return subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        encoding="utf-8",   # force UTF-8
        errors="replace",   # never crash on weird bytes
        timeout=timeout,
    )

def winget_available() -> bool:
    try:
        res = run_text(["winget", "--version"], timeout=8)
        return res.returncode == 0
    except Exception:
        return False

def winget_show_exact(pkg_id: str) -> bool:
    out = run_text(["winget", "show", "--id", pkg_id, "--exact"])
    stdout = (out.stdout or "").lower()
    return out.returncode == 0 and pkg_id.lower() in stdout

def winget_suggest(name_or_id: str) -> Optional[str]:
    """
    Try to find a better ID using `winget search`.
    Returns one likely ID (Publisher.Product) if we can extract it.
    """
    out = run_text(["winget", "search", name_or_id])
    if out.returncode != 0:
        return None

    lines = [ln.strip() for ln in (out.stdout or "").splitlines() if ln.strip()]
    candidates = []
    for ln in lines:
        # Winget formats in columns with 2+ spaces between
        cols = re.split(r"\s{2,}", ln)
        if len(cols) >= 2:
            maybe_id = cols[1].strip()
            # prefer fully-qualified IDs like Publisher.Product
            if "." in maybe_id and " " not in maybe_id and 1 < len(maybe_id) <= 80:
                candidates.append(maybe_id)

    # Return the first unique candidate if any
    if candidates:
        return candidates[0]
    return None

def github_latest_asset(ctx: Context, repo: str, pattern: Optional[str]) -> Optional[str]:
    """
    Returns the browser_download_url of the best-matching asset from latest release.
    If pattern is None, returns the first asset (prefer .msi/.exe/.zip).
    """
    base = f"https://api.github.com/repos/{repo}/releases/latest"
    r = ctx.session.get(base, timeout=TIMEOUT)
    if r.status_code != 200:
        return None
    assets = r.json().get("assets", [])
    if not assets:
        return None
    # Preferred order
    exts = [".msi", ".exe", ".zip", ".7z"]
    def score(name: str) -> int:
        # smaller score = better
        name_l = name.lower()
        for i, ext in enumerate(exts):
            if name_l.endswith(ext):
                return i
        return len(exts) + 1

    if pattern:
        patt = pattern.lower()
        matches = [a for a in assets if patt in a.get("name", "").lower()]
        assets_to_consider = matches if matches else assets
    else:
        assets_to_consider = assets

    assets_to_consider.sort(key=lambda a: score(a.get("name", "")))
    return assets_to_consider[0].get("browser_download_url")

def iter_install_methods(app: Dict[str, Any]) -> List[Tuple[str, Dict[str, Any]]]:
    """
    Returns a list of (style, method) where style is either legacy 'legacy' or 'method'
    so we can write back to the right place.
    """
    out = []
    if "install_type" in app and ("url" in app or "winget_id" in app or "github_repo" in app):
        out.append(("legacy", app))
    for m in app.get("install_methods", []):
        out.append(("method", m))
    return out

def audit_and_fix(ctx: Context) -> None:
    sess = ctx.session
    sess.headers.update({"User-Agent": "ExilesInstaller-LinkDoctor/1.0"})

    for app in ctx.config.get("apps", []):
        app_id = app.get("id") or app.get("name") or "UNKNOWN"
        app_name = app.get("name") or app_id

        for style, m in iter_install_methods(app):
            mtype = m.get("type") or m.get("install_type")
            # --- HTTP-like methods
            if mtype in {"web", "exe", "zip", "msi"} and m.get("url"):
                url = m["url"]
                ok, sc, final_url, note = check_url(sess, url)
                if ok:
                    # Normalize to final_url if it differs and is same domain; keep manual links intact
                    if final_url and final_url != url and not m.get("manual", False):
                        ctx.findings.append(Finding(app_id, app_name, "http",
                                                    "normalized URL after redirects",
                                                    old=url, new=final_url, note=note, fixed=False))
                        if not ctx.dry_run:
                            m["url"] = final_url
                    continue

                # If broken, try a domain root as fallback suggestion
                fallback = None
                try:
                    m_host = re.match(r"^https?://([^/]+)/", url)
                    if m_host:
                        fallback = f"https://{m_host.group(1)}/"
                except Exception:
                    pass

                ctx.findings.append(Finding(app_id, app_name, "http",
                                            f"HTTP link failed (status {sc})",
                                            old=url, new=fallback, note=note, fixed=False))
                # We don't auto-write fallback (manual review)
                continue

            # --- GitHub methods
            if mtype == "github" and m.get("github_repo"):
                repo = m["github_repo"]
                patt = m.get("github_asset")
                best = github_latest_asset(ctx, repo, patt)
                if best:
                    # Only auto-apply if this method looks like it's intended to download directly
                    if m.get("url"):
                        old = m["url"]
                        if old != best:
                            ctx.findings.append(Finding(app_id, app_name, "github",
                                                        "updated GitHub asset download URL",
                                                        old=old, new=best, fixed=True))
                            if not ctx.dry_run:
                                m["url"] = best
                    else:
                        # add a url key so the app can direct-download
                        ctx.findings.append(Finding(app_id, app_name, "github",
                                                    "added GitHub asset download URL",
                                                    old=None, new=best, fixed=True))
                        if not ctx.dry_run:
                            m["url"] = best
                else:
                    ctx.findings.append(Finding(app_id, app_name, "github",
                                                "no matching assets in latest release",
                                                old=patt or "", new=None, fixed=False))
                continue

            # --- winget methods
            if mtype == "winget" and m.get("winget_id"):
                pkg_id = m["winget_id"]
                if winget_available():
                    if winget_show_exact(pkg_id):
                        continue
                    # Try to suggest a likely correct ID
                    suggestion = winget_suggest(pkg_id) or winget_suggest(app_name) or winget_suggest(app_id)
                    if suggestion and suggestion.lower() != pkg_id.lower() and winget_show_exact(suggestion):
                        ctx.findings.append(Finding(app_id, app_name, "winget",
                                                    "updated winget id",
                                                    old=pkg_id, new=suggestion, fixed=True))
                        if not ctx.dry_run:
                            m["winget_id"] = suggestion
                    else:
                        ctx.findings.append(Finding(app_id, app_name, "winget",
                                                    "winget id not found; no unique suggestion",
                                                    old=pkg_id, new=None, fixed=False))
                else:
                    ctx.findings.append(Finding(app_id, app_name, "winget",
                                                "winget not available on this machine (skipped)",
                                                old=pkg_id, new=None, fixed=False))
                continue

def write_report(ctx: Context, path: Path) -> None:
    lines = []
    lines.append(f"# Link Doctor Report\n")
    lines.append(f"- Mode: {'DRY-RUN (no changes written)' if ctx.dry_run else 'FIXED (changes applied)'}")
    lines.append(f"- Source: `{APPS_JSON}`")
    lines.append("")
    if not ctx.findings:
        lines.append("✅ No issues found.")
    else:
        for f in ctx.findings:
            status = "✓" if f.fixed and not ctx.dry_run else ("→" if f.new else "✗")
            lines.append(f"## {status} {f.app_name} [{f.source}]")
            lines.append(f"- Message: {f.message}")
            if f.old: lines.append(f"- Old: `{f.old}`")
            if f.new: lines.append(f"- New: `{f.new}`")
            if f.note: lines.append(f"- Note: {f.note}")
            lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")

def main():
    parser = argparse.ArgumentParser(
        description="Audit and optionally auto-fix links in src/apps.json (HTTP, GitHub assets, winget IDs)."
    )
    parser.add_argument("--fix", action="store_true",
                        help="Apply safe auto-fixes (write back to apps.json). Always creates a backup.")
    parser.add_argument("--only", nargs="*", default=None,
                        help="Limit to specific app ids (space-separated).")
    parser.add_argument("--apps", default=str(APPS_JSON), help="Path to apps.json")
    args = parser.parse_args()

    apps_path = Path(args.apps).resolve()
    if not apps_path.exists():
        print(f"[error] apps.json not found at {apps_path}", file=sys.stderr)
        sys.exit(2)

    cfg = load_config(apps_path)
    if args.only:
        # Filter by ids
        ids = set(args.only)
        cfg = {**cfg, "apps": [a for a in cfg.get("apps", []) if (a.get("id") or a.get("name")) in ids]}

    ctx = Context(config=cfg, dry_run=(not args.fix))
    # Perform audit & fixes
    audit_and_fix(ctx)

    ARTIFACTS.mkdir(exist_ok=True)
    ts = time.strftime("%Y%m%d-%H%M%S")
    report = ARTIFACTS / f"link_report.{ts}.md"
    write_report(ctx, report)

    if args.fix:
        # Write back: load full file, merge fixes so we don't drop unrelated apps when --only is used.
        backup = backup_config(apps_path)
        full = load_config(apps_path)
        # Build index by id/name
        index: Dict[str, Dict[str, Any]] = {}
        def key(a: Dict[str, Any]) -> str:
            return (a.get("id") or a.get("name") or "").lower()

        for a in full.get("apps", []):
            index[key(a)] = a

        for updated in ctx.config.get("apps", []):
            k = key(updated)
            if not k: continue
            index[k].update(updated)
            # if updated has install_methods array with fixes, overwrite that array specifically
            if "install_methods" in updated:
                index[k]["install_methods"] = updated["install_methods"]
            # legacy fields (install_type/url/etc.) also copied over if present
            for fld in ("install_type","url","winget_id","github_repo","github_asset"):
                if fld in updated:
                    index[k][fld] = updated[fld]

        # Save back full
        save_config(apps_path, full)
        print(f"[ok] Wrote fixes to {apps_path} (backup: {backup})")
    else:
        print("[ok] DRY-RUN complete; no changes written.")
    print(f"[ok] Report: {report}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[warn] Aborted by user.")
        sys.exit(130)
    except Exception as e:
        print(f"[error] {e}", file=sys.stderr)
        sys.exit(1)
