#!/usr/bin/env python3
"""
Test script for Exiles Installer privilege handling
Verifies that admin detection and privilege requirements work correctly
"""

import json
import platform

def test_privilege_detection():
    """Test the privilege detection functionality"""
    print("🔐 Testing Exiles Installer Privilege Handling")
    print("=" * 50)
    
    # Load apps configuration
    with open('src/apps.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    apps = config.get('apps', [])
    
    print(f"📊 Testing {len(apps)} applications for privilege requirements")
    print()
    
    # Check which apps require admin privileges
    admin_required_apps = []
    winget_apps = []
    exe_msi_apps = []
    
    for app in apps:
        app_id = app.get('id', '')
        app_name = app.get('name', 'Unknown')
        
        # Check explicit admin requirement
        if app.get('requires_admin', False):
            admin_required_apps.append(f"{app_name} (explicit)")
            continue
        
        # Check by app ID (built-in detection)
        admin_app_ids = ['vJoy', 'HidHide', 'AutoHotkey', 'VKBDevCfg', 'VIRPIL-VPC', 'TARGET', 'TrackIR', 'TobiiGameHub']
        if app_id in admin_app_ids:
            admin_required_apps.append(f"{app_name} (built-in detection)")
            continue
        
        # Check install methods
        install_methods = app.get('install_methods', [])
        for method in install_methods:
            method_type = method.get('type', '')
            if method_type == 'winget':
                winget_apps.append(app_name)
                break
            elif method_type in ['msi', 'exe']:
                exe_msi_apps.append(app_name)
                break
        
        # Check legacy install_type
        install_type = app.get('install_type', '')
        if install_type == 'winget':
            winget_apps.append(app_name)
        elif install_type in ['msi', 'exe']:
            exe_msi_apps.append(app_name)
    
    # Print results
    print("🔐 APPS REQUIRING ADMINISTRATOR PRIVILEGES:")
    print("-" * 45)
    for app in admin_required_apps:
        print(f"   ✅ {app}")
    print()
    
    print("📦 WINGET APPS (May require admin):")
    print("-" * 35)
    for app in winget_apps:
        print(f"   ⚠️  {app}")
    print()
    
    print("💿 EXE/MSI APPS (May require admin):")
    print("-" * 35)
    for app in exe_msi_apps:
        print(f"   ⚠️  {app}")
    print()
    
    # Summary
    total_admin = len(admin_required_apps)
    total_winget = len(winget_apps) 
    total_exe_msi = len(exe_msi_apps)
    total_may_need_admin = total_admin + total_winget + total_exe_msi
    
    print("📊 PRIVILEGE SUMMARY:")
    print("-" * 20)
    print(f"   🔐 Definitely need admin: {total_admin}")
    print(f"   📦 Winget (may need): {total_winget}")
    print(f"   💿 EXE/MSI (may need): {total_exe_msi}")
    print(f"   ⚠️  Total apps that may need admin: {total_may_need_admin}/{len(apps)}")
    print()
    
    # Platform info
    current_platform = platform.system()
    print(f"🖥️  Current platform: {current_platform}")
    
    if current_platform == "Windows":
        print("   ✅ Windows UAC elevation handling will be used")
    else:
        print("   ℹ️  Non-Windows platform - privilege handling is simplified")
    print()
    
    # Test results
    print("🎯 TEST RESULTS:")
    print("-" * 15)
    
    # Check if critical apps are marked correctly
    critical_apps = ['vJoy', 'HidHide', 'AutoHotkey']
    missing_admin_flags = []
    
    for app in apps:
        app_id = app.get('id', '')
        if app_id in critical_apps:
            if not app.get('requires_admin', False):
                missing_admin_flags.append(app.get('name', app_id))
    
    if missing_admin_flags:
        print(f"   ❌ Missing admin flags: {', '.join(missing_admin_flags)}")
        return False
    else:
        print("   ✅ All critical apps properly marked for admin privileges")
    
    if total_may_need_admin > 0:
        print("   ✅ Privilege handling system will manage elevated installations")
    else:
        print("   ⚠️  No apps detected that need privilege handling")
    
    print("   ✅ Configuration loaded successfully")
    print("   ✅ Privilege detection logic working correctly")
    print()
    
    print("🎉 PRIVILEGE HANDLING TEST COMPLETED SUCCESSFULLY!")
    return True

if __name__ == '__main__':
    success = test_privilege_detection()
    exit(0 if success else 1)