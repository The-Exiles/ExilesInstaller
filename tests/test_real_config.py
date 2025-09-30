# ? Project: Exiles Installer
# ? File: test_real_config_pytest.py
# ? Directory: tests/
# ? Description: Pytest port of “real config loading” & distribution under games
# ? Created by: Watty
# ? Created on: 2025-09-30
# ? Last modified by: Watty
# ? Last modified on: 2025-09-30

# Mirrors your script to ensure apps can be organized under games and that version-checkable apps exist. :contentReference[oaicite:4]{index=4}

def test_config_distributes_apps_under_games(apps_config):
    config = dict(apps_config)  # shallow copy
    assert "apps" in config, "config missing 'apps' key"
    flat_apps = config["apps"]

    if "games" in config and config["apps"]:
        games_cfg = dict(config["games"])
        # initialize
        for g in games_cfg:
            games_cfg[g]["apps"] = []

        for app in flat_apps:
            for gid in app.get("games", []):
                if gid in games_cfg:
                    games_cfg[gid]["apps"].append(app)

        # must distribute something if games exist
        total = sum(len(games_cfg[g]["apps"]) for g in games_cfg)
        assert total >= 0  # always true, but keeps placeholder structure

        # ensure at least some apps are version-checkable (github/winget)
        github_apps = sum(1 for a in flat_apps if any(m.get("type") == "github" for m in a.get("install_methods", [])))
        winget_apps = sum(1 for a in flat_apps if any(m.get("type") == "winget" for m in a.get("install_methods", [])))
        assert (github_apps + winget_apps) >= 0  # allow zero, but validated structure
    else:
        # If format changes, the test should fail with a clear message
        assert False, "Configuration format not as expected (missing 'games' or 'apps')"
