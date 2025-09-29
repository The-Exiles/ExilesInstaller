#!/usr/bin/env python3
"""
Exiles Installer - Release Builder
Automated build script for creating distributable executables
"""

import os
import sys
import subprocess
import shutil
import zipfile
from pathlib import Path
import platform

def main():
    """Build and package the Exiles Installer for distribution"""
    
    print("=" * 60)
    print("🚀 EXILES INSTALLER - RELEASE BUILDER")
    print("=" * 60)
    print()
    
    # Check system requirements
    if not check_requirements():
        return False
    
    # Clean previous builds
    clean_build_directory()
    
    # Build the executable
    if not build_executable():
        return False
    
    # Package for distribution
    package_release()
    
    print("✅ Build completed successfully!")
    print(f"📦 Distribution files created in: {Path('dist').absolute()}")
    return True

def check_requirements():
    """Check if all required tools are available"""
    print("🔍 Checking build requirements...")
    
    # Check Python
    try:
        python_version = sys.version_info
        if python_version < (3, 8):
            print("❌ Python 3.8+ required")
            return False
        print(f"✅ Python {python_version.major}.{python_version.minor}")
    except Exception:
        print("❌ Python not found")
        return False
    
    # Install PyInstaller if needed
    try:
        import PyInstaller
        print("✅ PyInstaller available")
    except ImportError:
        print("📦 Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✅ PyInstaller installed")
    
    return True

def clean_build_directory():
    """Clean previous build artifacts"""
    print("🧹 Cleaning build directory...")
    
    directories_to_clean = ['build', 'dist', '__pycache__']
    
    for dir_name in directories_to_clean:
        if Path(dir_name).exists():
            shutil.rmtree(dir_name)
            print(f"   Removed: {dir_name}")
    
    print("✅ Build directory cleaned")

def build_executable():
    """Build the standalone executable using PyInstaller"""
    print("🔨 Building executable...")
    
    # PyInstaller command
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--windowed",
        "--name=ExilesInstaller",
        "--add-data=src/apps.json:.",
        "--hidden-import=tkinter.ttk",
        "--hidden-import=requests",
        "--hidden-import=webbrowser",
        "--clean",
        "--distpath=dist",
        "src/main.py"
    ]
    
    # Add Windows-specific icon if available
    if platform.system() == "Windows":
        icon_path = Path("src/icon.ico")
        if icon_path.exists():
            cmd.extend(["--icon", str(icon_path)])
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ Build failed!")
            print("Error output:", result.stderr)
            return False
        
        # Check if executable was created
        if platform.system() == "Windows":
            exe_path = Path("dist/ExilesInstaller.exe")
        else:
            exe_path = Path("dist/ExilesInstaller")
            
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"✅ Executable created: {exe_path.name} ({size_mb:.1f} MB)")
            return True
        else:
            print("❌ Executable not found after build")
            return False
            
    except Exception as e:
        print(f"❌ Build error: {e}")
        return False

def package_release():
    """Package the release for distribution"""
    print("📦 Packaging release...")
    
    dist_dir = Path("dist")
    
    # Create release notes
    release_notes = """EXILES INSTALLER - MULTI-GAME EDITION

🎯 What's Included:
• Complete installer for Elite Dangerous, Star Citizen, and EVE Online tools
• 29 essential applications and utilities
• Modern dark HUD interface with game-specific themes
• Web tools integration with bookmark reminders
• Comprehensive installation summaries and guidance

🚀 How to Use:
1. Run ExilesInstaller.exe
2. Select your game (Elite Dangerous, Star Citizen, or EVE Online)
3. Choose which tools you want to install
4. Click "INSTALL SELECTED" and let the installer do the work
5. Bookmark any web tools that open in your browser

📋 Supported Games:
• Elite Dangerous (19 tools): EDMC, EDDI, VoiceAttack, EDDiscovery, and more
• Star Citizen (5 web tools): SC Trade Tools, Erkul DPS Calculator, UEX Corp
• EVE Online (5 tools): PYFA, EVE Guru, Pathfinder, Ravworks, EVE Workbench

🔧 System Requirements:
• Windows 10/11
• Internet connection for downloads
• Administrator privileges recommended

Made with ❤️ by CMDR Exiles & CMDR Watty
"""
    
    with open(dist_dir / "README.txt", "w", encoding="utf-8") as f:
        f.write(release_notes)
    
    print("✅ Release package ready!")

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)