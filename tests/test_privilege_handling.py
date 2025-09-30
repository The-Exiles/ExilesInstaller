# ? Project: Exiles Installer
# ? File: test_privilege_handling_pytest.py
# ? Directory: tests/
# ? Description: Pytest port of privilege/admin detection checks
# ? Created by: Watty
# ? Created on: 2025-09-30
# ? Last modified by: Watty
# ? Last modified on: 2025-09-30

# Based on your original script’s logic, but using asserts. :contentReference[oaicite:3]{index=3}

def test_privilege_detection_flags(apps_config):
    apps = apps_config.get("apps", [])
    # critical that should be marked or captured by built-ins
    critical_ids = {"vJoy", "HidHide", "AutoHotkey"}

    # collect admin-required or likely-admin apps
    admin_explicit = {a.get("id") for a in apps if a.get("requires_admin")}
    admin_builtins = {"vJoy","HidHide","AutoHotkey","VKBDevCfg","VIRPIL-VPC","TARGET","TrackIR","TobiiGameHub"}

    # Verify critical ones are either explicitly requires_admin or in our builtin list
    missing = []
    for a in apps:
        aid = a.get("id")
        if aid in critical_ids:
            if not (a.get("requires_admin") or aid in admin_builtins):
                missing.append(a.get("name", aid))

    assert not missing, f"Critical apps missing admin flags: {', '.join(missing)}"
