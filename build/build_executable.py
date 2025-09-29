#!/usr/bin/env python3
"""
Build script for creating the Exiles Installer executable
"""

import subprocess
import sys
import os
from pathlib import Path

def build_executable():
    """Build the executable using PyInstaller"""
    try:
        print("=== Building Exiles Installer Executable ===\n")
        
        # PyInstaller command with optimal settings for the installer
        # Use correct path separator for the current OS
        data_separator = ':' if os.name == 'posix' else ';'
        
        cmd = [
            sys.executable, '-m', 'PyInstaller',
            '--onefile',                        # Single executable file
            '--windowed',                       # No console window (GUI app)
            '--name=ExilesInstaller',           # Output filename
            f'--add-data=apps.json{data_separator}.', # Include apps.json in the executable
            '--hidden-import=tkinter.ttk',      # Ensure tkinter components are included
            '--hidden-import=requests',         # Ensure requests is included
            '--clean',                          # Clean build directory
            '--distpath=dist',                  # Output directory
            'main.py'                           # Main script
        ]
        
        print("Running PyInstaller...")
        print(f"Command: {' '.join(cmd)}\n")
        
        # Run PyInstaller
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✓ PyInstaller completed successfully!")
            
            # Check if executable was created (different extensions on different platforms)
            exe_name = 'ExilesInstaller.exe' if os.name == 'nt' else 'ExilesInstaller'
            exe_path = Path('dist') / exe_name
            
            if exe_path.exists():
                size_mb = exe_path.stat().st_size / (1024 * 1024)
                print(f"✓ Executable created: {exe_path}")
                print(f"✓ File size: {size_mb:.1f} MB")
                return True
            else:
                # List what was actually created
                dist_files = list(Path('dist').glob('*')) if Path('dist').exists() else []
                print(f"✗ Expected executable not found: {exe_path}")
                print(f"Files in dist/: {[f.name for f in dist_files]}")
                return False
        else:
            print("✗ PyInstaller failed!")
            print(f"Error output: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"✗ Build failed: {e}")
        return False

def main():
    """Main build function"""
    success = build_executable()
    
    if success:
        print("\n=== Build Complete ===")
        print("The Exiles Installer executable is ready!")
        print("Location: dist/ExilesInstaller.exe")
        print("\nThis single executable file contains:")
        print("- The complete GUI installer")
        print("- All installation handlers")
        print("- The apps.json configuration")
        print("- All required dependencies")
        print("\nUsers can simply run ExilesInstaller.exe to install Elite Dangerous applications!")
    else:
        print("\n=== Build Failed ===")
        print("Please check the error messages above.")
        return False
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)