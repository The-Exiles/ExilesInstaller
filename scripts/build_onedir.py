# ? Project: Exiles Installer
# ? File: build_onedir.py
# ? Directory: scripts/
# ? Description: Build a fast-startup onedir PyInstaller bundle with versioned artifacts.
# ? Created by: Watty
# ? Created on: 2025-09-30
# ? Last modified by: Watty
# ? Last modified on: 2025-09-30

import os
import sys
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
DIST = ROOT / "dist"
BUILD = ROOT / "build"
ARTIFACTS = ROOT / "artifacts"
ICON = ROOT / "installer" / "icons" / "exiles.ico"

APP_NAME = "ExilesInstaller"
ENTRY = SRC / "main.py"

def detect_version() -> str:
    version = os.environ.get("EXILES_INSTALLER_VERSION", "").strip()
    if version:
        return version
    return datetime.now().strftime("%Y.%m.%d-%H%M")

def run(cmd: list[str]) -> None:
    print(">>", " ".join(cmd))
    subprocess.check_call(cmd)

def main() -> None:
    version = detect_version()
    ARTIFACTS.mkdir(exist_ok=True)

    if DIST.exists(): shutil.rmtree(DIST)
    if BUILD.exists(): shutil.rmtree(BUILD)

    pyinstaller_cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconfirm",
        "--onedir",
        "--windowed",
        f"--name={APP_NAME}",
        f"--icon={ICON}" if ICON.exists() else None,
        "--clean",
        "--collect-data=tcl",
        "--collect-data=tk",
        "--hidden-import=tkinter",
        "--hidden-import=tkinter.ttk",
        "--hidden-import=tkinter.messagebox",
        "--hidden-import=tkinter.filedialog",
        "--hidden-import=requests",
        "--hidden-import=webbrowser",
        str(ENTRY),
    ]

    # Remove None values before running
    pyinstaller_cmd = [arg for arg in pyinstaller_cmd if arg]

    pyinstaller_cmd = [a for a in pyinstaller_cmd if a]
    run(pyinstaller_cmd)

    app_dir = DIST / APP_NAME
    app_dir.mkdir(parents=True, exist_ok=True)
    for name in ("apps.json", "exiles_config.json"):
        src = SRC / name
        if src.exists():
            shutil.copy2(src, app_dir / name)

    portable_zip = ARTIFACTS / f"{APP_NAME}-portable-{version}.zip"
    if portable_zip.exists(): portable_zip.unlink()
    shutil.make_archive(portable_zip.with_suffix(""), "zip", DIST, APP_NAME)
    print(f"✓ Portable ZIP: {portable_zip}")

if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as e:
        print(f"[build] ERROR: command failed with exit code {e.returncode}", file=sys.stderr)
        sys.exit(e.returncode)
    except Exception as e:
        print(f"[build] ERROR: {e}", file=sys.stderr)
        sys.exit(1)
