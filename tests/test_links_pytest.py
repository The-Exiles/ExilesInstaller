# ? Project: Exiles Installer
# ? File: test_links_pytest.py
# ? Directory: tests/
# ? Description: Robust link/GitHub/winget checks with retries and actionable failure messages
# ? Created by: Watty
# ? Created on: 2025-09-30
# ? Last modified by: Watty
# ? Last modified on: 2025-09-30

from typing import Iterable
import subprocess
import pytest

OK_HEAD = {200, 301, 302, 303, 307, 308}
OK_ANY = set(range(200, 400))  # treat any successful GET/redirect as OK

def _check_url(session, name: str, url: str):
    """
    HEAD first; if odd code (204/401/403/405/404) then try GET before failing.
    Returns (ok: bool, status: int|None, note: str|None)
    """
    try:
        r = session.head(url, timeout=12, allow_redirects=True)
        sc = r.status_code
        if sc in OK_HEAD:
            return True, sc, None
        # Try GET for sites that hate HEAD (common) or return 204 on home
        r = session.get(url, timeout=15, stream=True, allow_redirects=True)
        r.close()
        sc = r.status_code
        if sc in OK_ANY:
            return True, sc, "passed on GET"
        return False, sc, None
    except Exception as e:
        return False, None, f"exception: {e}"

@pytest.mark.slow
def test_http_links_ok(apps_config, http):
    apps = apps_config.get("apps", [])
    failures = []
    for app in apps:
        # legacy single install_type
        if "install_type" in app and "url" in app and app["install_type"] in {"web","exe","zip","msi"}:
            ok, sc, note = _check_url(http, app.get("name"), app["url"])
            if not ok:
                failures.append((app.get("name"), app["url"], sc, note))

        # new install_methods
        for m in app.get("install_methods", []):
            if m.get("type") in {"web","exe","zip","msi"} and m.get("url"):
                ok, sc, note = _check_url(http, app.get("name"), m["url"])
                if not ok:
                    failures.append((app.get("name"), m["url"], sc, note))

    assert not failures, "Broken HTTP links:\n" + "\n".join(
        f"{n}: {u} [HTTP {sc if sc is not None else '?'}]{' ('+note+')' if note else ''}"
        for n,u,sc,note in failures
    )

@pytest.mark.slow
def test_github_repos_exist(apps_config, http):
    base = "https://api.github.com/repos/"
    max_calls = 60
    calls = 0

    def get(url, **kw):
        nonlocal calls
        if calls >= max_calls:
            return None
        calls += 1
        return http.get(url, timeout=12, **kw)

    failures = []
    for app in apps_config.get("apps", []):
        def check_repo(repo: str, asset_pattern: str|None):
            r = get(base + repo)
            if not r or r.status_code != 200:
                failures.append((app.get("name"), repo, f"repo missing/HTTP {r.status_code if r else 'rate-limit'}"))
                return
            if asset_pattern:
                rel = get(base + repo + "/releases/latest")
                if rel and rel.status_code == 200:
                    assets = rel.json().get("assets", [])
                    names = [a["name"] for a in assets]
                    patt = asset_pattern.lower()
                    if not any(patt in n.lower() for n in names):
                        failures.append((app.get("name"), repo, f"asset '{asset_pattern}' not found. saw: {', '.join(names)[:200]}"))
                else:
                    failures.append((app.get("name"), repo, "no releases/latest or HTTP error"))

        # legacy fields
        if app.get("install_type") == "github" and app.get("github_repo"):
            check_repo(app["github_repo"], app.get("github_asset"))
        # new install_methods
        for m in app.get("install_methods", []):
            if m.get("type") == "github" and m.get("github_repo"):
                check_repo(m["github_repo"], m.get("github_asset"))

    assert not failures, "GitHub repo/assets issues:\n" + "\n".join(
        f"{n}: {repo} -> {msg}" for n,repo,msg in failures
    )

# --- winget test (Windows-safe decoding) -------------------------------------

def _run_text(cmd, timeout=35):
    # ! important: Force UTF-8 + errors='replace' to avoid UnicodeDecodeError and None stdout
    return subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
    )

@pytest.mark.slow
def test_winget_packages_available(apps_config):
    try:
        res = _run_text(["winget","--version"], timeout=10)
        if res.returncode != 0:
            pytest.skip("winget not available on this system")
    except FileNotFoundError:
        pytest.skip("winget not installed on this system")

    def check_id(pid: str):
        out = _run_text(["winget","show","--id", pid, "--exact"])
        stdout = (out.stdout or "").lower()
        return out.returncode == 0 and pid.lower() in stdout

    failures = []
    for app in apps_config.get("apps", []):
        # legacy
        if app.get("install_type") == "winget" and app.get("winget_id"):
            if not check_id(app["winget_id"]):
                failures.append((app.get("name"), app["winget_id"]))
        # new
        for m in app.get("install_methods", []):
            if m.get("type") == "winget" and m.get("winget_id"):
                if not check_id(m["winget_id"]):
                    failures.append((app.get("name"), m["winget_id"]))

    assert not failures, (
        "winget packages not found:\n" +
        "\n".join(f"{n}: {pid} (try corrected IDs like Nefarius.HidHide, AutoHotkey.AutoHotkey)" for n,pid in failures)
    )
