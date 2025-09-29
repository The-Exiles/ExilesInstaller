# Exiles Installer - Multi-Game Edition

A comprehensive desktop application for space simulation gaming communities that automates the installation of third-party tools, utilities, and hardware drivers. Built with Python and Tkinter, featuring a dark spaceship HUD interface with multi-game support for **Elite Dangerous**, **Star Citizen**, and **EVE Online**.

![Multi-Game Support](https://img.shields.io/badge/Games-Elite%20Dangerous%20|%20Star%20Citizen%20|%20EVE%20Online-blue)
![Python](https://img.shields.io/badge/Python-3.8+-green)
![Platform](https://img.shields.io/badge/Platform-Windows%2010/11-blue)

## 🎯 Overview

The Exiles Installer provides a unified interface for installing essential tools across three major space simulation games. Whether you're a Commander, Pilot, or Capsuleer, this installer streamlines the setup of your gaming ecosystem with just a few clicks.

## ✨ Key Features

### 🎮 **Multi-Game Support**
- **Elite Dangerous**: 19 essential tools and utilities
- **Star Citizen**: 5 web-based tools and calculators  
- **EVE Online**: 5 tools including both desktop and web applications

### 🖥️ **Modern Interface**
- Dark spaceship HUD interface with Elite Dangerous theming
- Game-specific UI that adapts to your selected game
- Real-time progress tracking and comprehensive logging
- Intuitive card-based application selection

### 📦 **Multiple Installation Methods**
- **GitHub Releases**: Automatic latest version detection
- **Direct Downloads**: Executable and archive files
- **Windows Package Managers**: Winget and Chocolatey integration
- **Web Tools**: Browser-based applications with bookmark reminders
- **ZIP Archives**: Extraction with post-processing scripts

### 🔧 **Advanced Features**
- Streaming downloads with SHA-256 checksum verification
- Game switching with automatic tool filtering
- Comprehensive installation summaries with next steps
- Post-installation automation via PowerShell scripts
- Settings panel for customization

## 🎮 Supported Games & Tools

### Elite Dangerous (19 Tools)

#### Core Tools
- **ED Market Connector (EDMC)** - Essential market data uploader
- **EDDiscovery** - Exploration and travel tracking
- **EDDI Voice Response System** - Spoken game event information
- **EDEngineer** - Engineering materials tracker
- **EDHM-UI** - HUD color customization tool

#### Hardware & Input
- **Joystick Gremlin** - Advanced joystick configuration
- **vJoy** - Virtual joystick driver  
- **HidHide** - Device hiding utility
- **VoiceAttack** - Voice control software

#### Head Tracking
- **OpenTrack** - Open source head tracking
- **TrackIR** - Natural Point head tracking hardware
- **Tobii Game Hub** - Eye tracking integration

#### Manufacturer Tools
- **VIRPIL VPC** - VIRPIL hardware configuration
- **VKB DevCfg** - VKB joystick configuration
- **Thrustmaster TARGET** - Thrustmaster HOTAS software
- **Logitech G HUB** - Logitech gaming peripherals

#### Utilities
- **AutoHotkey v2** - Automation scripting
- **7-Zip** - File archiver
- **EDMC Overlay Plugin** - In-game information overlay

### Star Citizen (5 Web Tools)

- **SC Trade Tools** - Primary trade route optimization platform
- **Erkul DPS Calculator** - Ship loadout builder and DPS calculator  
- **UEX Corporation** - Comprehensive trading and mining data
- **CCU Game** - Ship upgrade chain optimization
- **GameGlass** - Touchscreen controls for Star Citizen

### EVE Online (5 Tools)

- **PYFA** - Python Fitting Assistant (desktop application)
- **EVE Guru** - Manufacturing planner with profitability optimization
- **Ravworks** - Free market and industry tool
- **Pathfinder** - Wormhole mapping and fleet management
- **EVE Workbench** - Web-based fitting and market tools

## 🚀 Quick Start

### Download & Run
1. Download `ExilesInstaller.exe` from releases
2. Run the executable (no installation required)
3. Select your game from the dropdown menu
4. Choose which tools you want to install
5. Click "► INSTALL SELECTED" and wait for completion

### First-Time Setup
1. **Elite Dangerous users**: Select essential tools like EDMC and EDDI
2. **Star Citizen pilots**: All tools are web-based - bookmark them when they open
3. **EVE Online capsuleers**: Install PYFA locally, bookmark web tools

## 🔧 Building from Source

### Prerequisites
- Windows 10/11 (target platform)
- Python 3.8 or later
- Internet connection

### Quick Build
```bash
# Using the automated build script
python build_release.py
```

### Manual Build
```bash
# Install dependencies
pip install -r requirements.txt
pip install pyinstaller

# Build executable
cd build
build_windows.bat
```

The executable will be created as `dist/ExilesInstaller.exe`

## 📋 Configuration

### Application Catalog
The application catalog is defined in `src/apps.json` with a multi-game structure:

```json
{
  "games": {
    "elite_dangerous": {
      "name": "Elite Dangerous",
      "apps": [...]
    },
    "star_citizen": {
      "name": "Star Citizen", 
      "apps": [...]
    },
    "eve_online": {
      "name": "EVE Online",
      "apps": [...]
    }
  }
}
```

### Application Entry Format
```json
{
  "id": "unique_id",
  "name": "Display Name",
  "install_type": "github|exe|web|winget|zip",
  "description": "Tool description",
  "optional": true,
  "url": "download_url",
  "checksum": "sha256_hash"
}
```

## 🏗️ Project Structure

```
Exiles-Installer/
├── src/
│   ├── main.py              # Main application
│   ├── apps.json            # Multi-game application catalog
│   └── exiles_config.json   # User settings
├── build/
│   ├── build_windows.bat    # Windows build script
│   └── test_installer.py    # Test suite  
├── docs/
│   ├── README.md            # This file
│   ├── USER_GUIDE.md        # User documentation
│   ├── DEVELOPER_GUIDE.md   # Developer documentation
│   └── BUILD_GUIDE.md       # Build instructions
├── build_release.py         # Automated build script
├── requirements.txt         # Python dependencies
└── replit.md               # Project documentation
```

## 🔐 Security & Safety

- **Checksum Verification**: Optional SHA-256 validation for downloads
- **Streaming Downloads**: Prevents memory exhaustion on large files
- **Sandboxed Execution**: PowerShell scripts limited to post-installation tasks
- **No Elevation**: Most applications install in user space
- **Web Tool Safety**: Browser isolation for web-based tools

## 🌐 Deployment Options

### Cloud Showcase (Replit)
- Interactive demo via VNC in web browser
- Try before downloading
- Always up-to-date version

### Local Distribution
- Single executable file (~20MB)
- No installation required
- Portable and self-contained

## 🆘 Troubleshooting

### Common Issues
1. **Installation Failures**: Run as Administrator
2. **Download Errors**: Check internet connection
3. **Antivirus Blocking**: Temporarily disable during installation
4. **Missing Dependencies**: Ensure Windows Package Manager is available

### Getting Help
1. Check the installation log for detailed error information
2. Verify all prerequisites are met
3. Try running individual tool installations manually
4. Contact support with log files if issues persist

## 🤝 Contributing

The installer is designed to be easily extensible. To add new games or tools:

1. Update `src/apps.json` with new entries
2. Test the configuration
3. Rebuild the executable
4. Submit pull request with documentation

## 📄 License

This project is designed for the Elite Dangerous, Star Citizen, and EVE Online gaming communities. All third-party tools retain their original licenses and copyrights.

---

**Made with ❤️ by CMDR Exiles & CMDR Watty**

*Fly safe, Commanders. See you in the black, Pilots. Good hunting, Capsuleers.*