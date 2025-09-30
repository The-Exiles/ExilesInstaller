# Exiles Installer - Build Guide

## 🎯 Overview

This guide covers building the Exiles Installer from source into a distributable Windows application. We use PyInstaller with the provided ExilesInstaller.spec to produce an onedir build (an app folder containing ExilesInstaller.exe and all dependencies). Optionally, you can package that folder into a Windows installer using Inno Setup (installer/ExilesInstaller.iss).

## 📋 Prerequisites

### System Requirements
- **Operating System**: Windows 10/11 (target platform)
- **Python**: Version 3.11 or later
- **Memory**: 4GB RAM minimum (for build process)
- **Disk Space**: 500MB free space for build artifacts
- **Internet**: Required for downloading PyInstaller and dependencies

### Development Tools
- **Git**: For source code management (optional)
- **Python pip**: Package installer (included with Python)
- **Windows Terminal**: Recommended for better command-line experience

## 🚀 Quick Build (Recommended)

From the repository root:

```powershell
# 1) (optional) Create/activate venv
python -m venv .venv
. .\.venv\Scripts\Activate.ps1

# 2) Install dependencies
pip install -r requirements.txt

# 3) Auto-fix links and run sanity tests
python .\scripts\link_doctor.py --fix
pytest -q          # or: pytest -q --runslow

# 4) Build portable onedir app (also zips into artifacts\)
python .\scripts\build_onedir.py

# 5) Build Windows installer (Inno Setup)
pwsh .\scripts\make_installer_inno.ps1
```
## ✅ Checksums (optional)

Generate and publish SHA-256 hashes for release assets:

```powershell
# Write SHA256SUMS.txt for all artifacts
Get-ChildItem .\artifacts\ExilesInstaller-*.* |
  ForEach-Object {
    $h = Get-FileHash $_ -Algorithm SHA256
    "$($h.Hash)  $($_.Name)"
  } | Out-File .\artifacts\SHA256SUMS.txt -Encoding ascii
```

### Build Output
```
dist/
└── ExilesInstaller/
├── ExilesInstaller.exe
└── _internal/…

artifacts/
├── ExilesInstaller-portable-<version>.zip
├── ExilesInstaller-<version>-Setup.exe
└── SHA256SUMS.txt (if enabled in script)
```

## 🔧 Alternative: Build using the PyInstaller spec

### Step 1: Setup Environment

```bash
# Install required dependencies
pip install -r requirements.txt

# Install PyInstaller
pip install pyinstaller

# Verify installation
pyinstaller --version
```

### Step 2: Clean Previous Builds

```bash
# Remove old build artifacts
rmdir /s build dist __pycache__
```

### Step 3: Build Executable

```powershell
# Build using the provided PyInstaller spec (onedir output)
# From the repository root
python -m pip install -r requirements.txt
python -m PyInstaller -y ExilesInstaller.spec
```

### Step 4: Verify Build

```powershell
# Check if executable was created
Get-Item dist\ExilesInstaller\ExilesInstaller.exe

# Test the executable
& "dist\ExilesInstaller\ExilesInstaller.exe"
```

## 🔧 Build Configuration

### PyInstaller Options Explained

| Option | Purpose |
|--------|---------|
| `--onefile` | Creates single executable (no DLL hell) |
| `--windowed` | Hides console window (GUI-only) |
| `--name=ExilesInstaller` | Sets output filename |
| `--add-data=src/apps.json:.` | Bundles JSON config into executable |
| `--hidden-import=tkinter.ttk` | Ensures GUI components are included |
| `--hidden-import=requests` | Forces HTTP client inclusion |
| `--hidden-import=webbrowser` | Browser integration support |
| `--clean` | Fresh build (removes cache) |
| `--distpath=dist` | Output directory |

### Configuration File Method

Create `installer.spec` for advanced builds:

```python
# installer.spec
import os

block_cipher = None

a = Analysis(
    ['src/main.py'],
    pathex=[os.getcwd()],
    binaries=[],
    datas=[('src/apps.json', '.')],
    hiddenimports=[
        'tkinter.ttk',
        'requests',
        'webbrowser',
        'hashlib',
        'zipfile',
        'subprocess',
        'threading'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='ExilesInstaller',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
```

Build with spec file:
```bash
pyinstaller installer.spec
```

## 🎨 Customization Options

### Adding Application Icon

1. Create or obtain an `.ico` file
2. Place it in the `src/` directory as `icon.ico`
3. Add to build command:

```bash
pyinstaller --icon=src/icon.ico [other options] src/main.py
```

### Version Information (Windows)

Create `version_info.txt`:
```
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(2,0,0,0),
    prodvers=(2,0,0,0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo([
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'CMDR Exiles'),
         StringStruct(u'FileDescription', u'Multi-Game Space Simulation Tools Installer'),
         StringStruct(u'FileVersion', u'2.0.0.0'),
         StringStruct(u'InternalName', u'ExilesInstaller'),
         StringStruct(u'LegalCopyright', u'© 2025 CMDR Exiles & CMDR Watty'),
         StringStruct(u'OriginalFilename', u'ExilesInstaller.exe'),
         StringStruct(u'ProductName', u'Exiles Installer - Multi-Game Edition'),
         StringStruct(u'ProductVersion', u'2.0.0.0')])
    ]), 
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
```

Add to build:
```bash
pyinstaller --version-file=version_info.txt [other options] src/main.py
```

## 🐛 Troubleshooting

### Common Build Issues

#### ImportError: No module named 'xyz'
```bash
# Solution: Add hidden import
pyinstaller --hidden-import=xyz [other options] src/main.py
```

#### Large Executable Size
```bash
# Check what's included
pyinstaller --onefile --log-level=DEBUG src/main.py

# Exclude unnecessary modules
pyinstaller --exclude-module=matplotlib [other options] src/main.py
```

#### Missing Data Files
```bash
# Ensure JSON config is included
pyinstaller --add-data=src/apps.json:. [other options] src/main.py

# For multiple data files
pyinstaller --add-data=src/apps.json:. --add-data=src/settings.ini:. src/main.py
```

#### Runtime Errors
```bash
# Build with debug console for testing
pyinstaller --onefile --console src/main.py

# Check for missing DLLs
depends.exe dist/ExilesInstaller.exe
```

### Build Performance

#### Faster Builds
```bash
# Use incremental builds (keep cache)
pyinstaller --noconfirm [other options] src/main.py

# Parallel processing
pyinstaller --multiprocess [other options] src/main.py
```

#### Smaller Executables
```bash
# Use UPX compression
pyinstaller --upx-dir=C:\upx [other options] src/main.py

# Exclude unused modules
pyinstaller --exclude-module=tkinter.dnd2 [other options] src/main.py
```

## 🧪 Testing Built Executable

### Functional Testing
```bash
# Test on clean Windows VM
# - No Python installed
# - No development tools
# - Fresh user account

# Verify all installation types work
# - GitHub releases
# - Direct downloads  
# - Web tools
# - Package managers
```

### Compatibility Testing
- **Windows 10**: All editions (Home, Pro, Enterprise)
- **Windows 11**: All current versions
- **Architecture**: x64 (primary), x86 (if needed)
- **Antivirus**: Test with Windows Defender and major AV solutions

### Performance Testing
```bash
# Monitor resource usage
# - Memory consumption during builds
# - Startup time on slow hardware
# - Download performance with slow internet
# - Installation time for full tool sets
```

## 📦 Packaging for Distribution

### Creating Release Package

```bash
# Create distribution folder
mkdir release
copy dist\ExilesInstaller.exe release\
copy docs\*.md release\docs\

# Create ZIP for distribution
7z a -tzip ExilesInstaller-v2.0.0.zip release\*
```

### Release Notes Template
```markdown
# Exiles Installer v2.0.0 - Multi-Game Edition

## 🎮 What's New
- Added Star Citizen support (5 web tools)
- Added EVE Online support (5 tools)
- Enhanced bookmark reminders for web tools
- Improved installation summaries

## 📥 Download & Install
1. Download ExilesInstaller.exe
2. Run the executable (no installation required)
3. Select your game and desired tools
4. Click "Install Selected"

## 🔧 System Requirements
- Windows 10/11
- Internet connection
- ~50MB disk space for installer + tools

## 🎯 Supported Games
- Elite Dangerous (19 tools)
- Star Citizen (5 web tools)  
- EVE Online (5 tools)

## 🐛 Known Issues
- None currently reported

## 📋 SHA-256 Checksums
ExilesInstaller.exe: [checksum here]
```

## 🚀 Automated Build Pipeline

### GitHub Actions Example
```yaml
name: Build Installer

on:
  push:
    tags: ['v*']

jobs:
  build:
    runs-on: windows-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
        
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pyinstaller
        
    - name: Build executable
      run: python -m PyInstaller -y ExilesInstaller.spec
      
    - name: Upload artifact
      uses: actions/upload-artifact@v3
      with:
        name: ExilesInstaller
        path: dist/
```

### Local Batch Build Script
```batch
@echo off
REM build_all.bat - Complete build and package script

echo === Exiles Installer Build Pipeline ===
echo.

REM Step 1: Clean environment
echo [1/5] Cleaning build environment...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist __pycache__ rmdir /s /q __pycache__

REM Step 2: Install dependencies
echo [2/5] Installing dependencies...
pip install -r requirements.txt
pip install pyinstaller

REM Step 3: Build executable
echo [3/5] Building executable...
python -m PyInstaller -y ExilesInstaller.spec

REM Step 4: Test executable
echo [4/5] Testing executable...
if exist dist\ExilesInstaller\ExilesInstaller.exe (
    echo Build successful!
    echo File size: 
    for %%I in (dist\ExilesInstaller\ExilesInstaller.exe) do echo %%~zI bytes
) else (
    echo Build failed!
    pause
    exit /b 1
)

REM Step 5: Package for distribution
echo [5/5] Creating distribution package...
mkdir release 2>nul
copy dist\ExilesInstaller.exe release\
copy docs\*.md release\docs\ 2>nul

echo.
echo === Build Complete ===
echo Distribution ready in: release\
echo.
pause
```

---

## 🤝 Contributing to Build Process

### Improving Build Scripts
- Optimize build time and executable size
- Add cross-platform support for Linux/macOS
- Implement automated testing in build pipeline
- Add code signing for distribution

### Documentation Updates
- Keep build instructions current with PyInstaller updates
- Document new customization options
- Add troubleshooting for new issues

*Happy building! Create something amazing for the space simulation community.*