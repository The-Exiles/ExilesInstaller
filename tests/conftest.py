# ? Project: Exiles Installer
# ? File: conftest.py
# ? Directory: tests/
# ? Description: Shared pytest fixtures/helpers (robust apps.json loader, HTTP session)
# ? Created by: Watty
# ? Created on: 2025-09-30
# ? Last modified by: Watty
# ? Last modified on: 2025-09-30

from pathlib import Path
import json
import os
import pytest
import requests

@pytest.fixture(scope="session")
def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]

@pytest.fixture(scope="session")
def apps_config(repo_root):
    """
    Robustly load src/apps.json regardless of where pytest is invoked from.
    """
    candidates = [
        repo_root / "src" / "apps.json",
        Path("src/apps.json").resolve(),
        (Path(__file__).resolve().parent / "../src/apps.json").resolve(),
    ]
    for p in candidates:
        if p.exists():
            with open(p, "r", encoding="utf-8") as f:
                return json.load(f)
    raise FileNotFoundError(f"apps.json not found. Looked in: {', '.join(map(str, candidates))}")

@pytest.fixture(scope="session")
def http():
    s = requests.Session()
    s.headers.update({"User-Agent": "ExilesInstaller-Tests/1.0"})
    return s

def pytest_addoption(parser):
    parser.addoption(
        "--runslow",
        action="store_true",
        default=False,
        help="run slow tests (e.g., network/winget)",
    )

def pytest_collection_modifyitems(config, items):
    if config.getoption("--runslow"):
        return
    skip_slow = pytest.mark.skip(reason="--runslow not provided")
    for item in items:
        if "slow" in item.keywords:
            item.add_marker(skip_slow)
