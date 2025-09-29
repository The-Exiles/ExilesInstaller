# Exiles Installer

A comprehensive desktop application for the Elite Dangerous gaming community that automates the installation of third-party tools, utilities, and hardware drivers. Built with Python and Tkinter, featuring a dark spaceship HUD interface inspired by Elite Dangerous.

## Features

- **Elite Dangerous themed GUI** - Dark spaceship HUD interface with orange and blue accents
- **Multi-source installation support**:
  - Windows Package Manager (winget)
  - Chocolatey package manager  
  - GitHub releases (automatic latest version detection)
  - Direct executable downloads
  - ZIP archive extraction with post-processing
- **Streaming downloads** with optional SHA-256 checksum verification
- **Comprehensive logging** with both GUI feedback and log files
- **Post-installation automation** via PowerShell scripts
- **Single executable** - No installation required, just run the .exe file

## Included Applications

The installer includes 19 essential Elite Dangerous applications:

### Core Tools
- **ED Market Connector (EDMC)** - Essential tool for uploading market data
- **EDDiscovery** - Comprehensive exploration and travel tracking
- **EDDI Voice Response System** - Spoken information about game events

### Observatory Plugins  
- **Observatory Core** - Plugin framework for Elite Dangerous
- **OD Elite Tracker** - Ship tracking and exploration data
- **ICARUS Terminal** - Advanced ship computer interface

### Hardware & Input
- **Joystick Gremlin** - Advanced joystick configuration
- **vJoy** - Virtual joystick driver
- **HidHide** - Device hiding utility
- **VoiceAttack** - Voice control software

### Head Tracking
- **OpenTrack** - Open source head tracking
- **TrackIR** - Natural Point head tracking
- **Tobii Game Hub** - Eye tracking integration

### Hardware Manufacturer Tools
- **VIRPIL VPC** - VIRPIL hardware configuration
- **VKB DevCfg** - VKB joystick configuration  
- **Thrustmaster TARGET** - Thrustmaster HOTAS software
- **Logitech Gaming Software** - Logitech device management

### Utilities
- **AutoHotkey** - Automation scripting
- **7-Zip** - File archiver

## Building for Windows

Since this application is designed for Windows users (Elite Dangerous players), you need to build it on a Windows machine:

### Prerequisites
- Windows 10/11
- Python 3.8 or later
- Internet connection for downloading PyInstaller

### Build Steps
1. Download or clone this project to your Windows machine
2. Open Command Prompt or PowerShell in the project directory
3. Run the build script:
   ```cmd
   cd build
   build_windows.bat
   ```
4. The executable will be created as `dist/ExilesInstaller.exe`

### Manual Build (if batch file doesn't work)
```cmd
pip install pyinstaller
cd src
pyinstaller --onefile --windowed --name=ExilesInstaller --add-data=apps.json;. --hidden-import=tkinter.ttk --hidden-import=requests main.py
```

## Usage

1. Download `ExilesInstaller.exe` to your Windows computer
2. Run the executable (no installation required)
3. Select which applications you want to install
4. Click "INSTALL SELECTED" and wait for completion
5. Check the log for installation status and any errors

## Configuration

The application catalog is defined in `src/apps.json`. To add new applications or update existing ones:

1. Edit the JSON file with the new application details
2. Rebuild the executable
3. Distribute the new version

Each application entry supports:
- `install_type`: "winget", "github", "exe", "zip"
- `optional`: true/false (affects default selection)
- `checksum`: SHA-256 hash for security validation (optional)
- `post_steps`: PowerShell scripts to run after installation

## File Structure

```
Exiles-Installer/
├── src/
│   ├── main.py           # Main application code
│   └── apps.json         # Application catalog
├── build/
│   ├── build_windows.bat # Windows build script
│   ├── build_executable.py # Cross-platform build script
│   └── test_installer.py   # Test suite
├── docs/
│   └── README.md         # This file
├── dist/                 # Built executables (created during build)
└── requirements.txt      # Python dependencies
```

## Technical Details

- **Framework**: Python 3.11+ with Tkinter GUI
- **Dependencies**: requests, pathlib, zipfile, hashlib
- **Build Tool**: PyInstaller for single-executable packaging
- **Target Platform**: Windows 10/11 (Elite Dangerous requirement)
- **Size**: ~18-20 MB executable (includes all dependencies)

## Security

- Optional SHA-256 checksum verification for downloads
- Streaming downloads to prevent memory exhaustion
- PowerShell execution limited to configured post-installation steps
- No elevation required for most applications (user-space installation)

## Support

This installer is designed to work with the standard Elite Dangerous gaming setup on Windows. For issues:

1. Check the log file generated during installation
2. Verify internet connectivity for downloads
3. Ensure Windows Package Manager (winget) is available on Windows 10/11
4. Run as administrator if individual application installations fail

The installer gracefully handles partial failures - if some applications fail to install, others will continue processing.