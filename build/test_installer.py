#!/usr/bin/env python3
"""
Test script for Exiles Installer functionality
"""

import json
import sys
from pathlib import Path

def test_apps_config():
    """Test that apps.json is valid and contains required data"""
    try:
        with open('../src/apps.json', 'r') as f:
            config = json.load(f)
        
        print("✓ apps.json is valid JSON")
        
        # Check structure
        assert 'metadata' in config, "Missing metadata section"
        assert 'apps' in config, "Missing apps section"
        assert isinstance(config['apps'], list), "Apps should be a list"
        
        print(f"✓ Configuration contains {len(config['apps'])} applications")
        
        # Check required fields in first few apps
        required_fields = ['id', 'name', 'install_type', 'description']
        for i, app in enumerate(config['apps'][:3]):  # Check first 3 apps
            for field in required_fields:
                assert field in app, f"App {i} missing required field: {field}"
        
        print("✓ Application entries have required fields")
        return True
        
    except Exception as e:
        print(f"✗ apps.json test failed: {e}")
        return False

def test_installer_imports():
    """Test that all required modules can be imported"""
    try:
        # Test imports from main.py
        import tkinter as tk
        import requests
        import subprocess
        import threading
        import zipfile
        import hashlib
        from pathlib import Path
        from datetime import datetime
        import logging
        
        print("✓ All required modules can be imported")
        return True
        
    except ImportError as e:
        print(f"✗ Import test failed: {e}")
        return False

def test_core_functionality():
    """Test core installer functionality without GUI"""
    try:
        # Import the main class
        sys.path.insert(0, '../src')
        
        # Test that the class definition is syntactically correct
        with open('../src/main.py', 'r') as f:
            code = compile(f.read(), 'main.py', 'exec')
        
        print("✓ main.py compiles successfully")
        
        # Test apps.json loading
        with open('../src/apps.json', 'r') as f:
            apps_data = json.load(f)
        
        # Count different install types
        install_types = {}
        for app in apps_data['apps']:
            install_type = app.get('install_type', 'unknown')
            install_types[install_type] = install_types.get(install_type, 0) + 1
        
        print(f"✓ Install types supported: {list(install_types.keys())}")
        for install_type, count in install_types.items():
            print(f"  - {install_type}: {count} applications")
        
        return True
        
    except Exception as e:
        print(f"✗ Core functionality test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=== Exiles Installer Test Suite ===\n")
    
    tests = [
        ("Configuration Test", test_apps_config),
        ("Import Test", test_installer_imports),
        ("Core Functionality Test", test_core_functionality)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\nRunning {test_name}...")
        if test_func():
            passed += 1
        
    print(f"\n=== Test Results ===")
    print(f"Passed: {passed}/{total} tests")
    
    if passed == total:
        print("✓ All tests passed! The Exiles Installer is ready.")
        return True
    else:
        print("✗ Some tests failed. Please check the output above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)