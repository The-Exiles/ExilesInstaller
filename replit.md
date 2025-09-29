# Exiles Installer - Multi-Game Ecosystem

## Overview

Exiles Installer is a comprehensive desktop application for gaming communities that automates the installation of third-party tools, utilities, and hardware drivers. Built with Python and Tkinter, it provides a centralized solution for installing gaming ecosystems including market connectors, exploration tools, voice response systems, joystick software, head tracking applications, and various hardware manufacturer utilities.

**PROJECT STATUS: COMPLETE** - The application has successfully expanded to support three major space simulation gaming ecosystems: Elite Dangerous, Star Citizen, and EVE Online. The installer now provides a unified interface for 29 essential tools across all three games, featuring modern multi-game architecture, comprehensive installation methods, and enhanced user experience.

The installer features a dark spaceship HUD interface, game-specific tool filtering, web-based tool integration with bookmark reminders, enhanced completion summaries, and complete deployment configuration. It's designed to be the definitive tool for setting up space simulation gaming environments with professional-grade features and documentation.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Application Structure
The application follows a monolithic desktop architecture built with Python's Tkinter framework. The main application (`main.py`) contains a single `ExilesInstaller` class that handles all GUI interactions, installation logic, and user interface management. This design choice prioritizes simplicity and ease of maintenance over modularity, making it suitable for a specialized installer application.

### Configuration Management
The application uses a JSON-based configuration system (`apps.json`) that defines all available applications and their installation parameters. This approach allows for easy modification of the application catalog without code changes. Each application entry includes metadata such as installation type, source URLs, optional flags, and post-installation scripts.

### Installation Methods
The installer supports multiple installation strategies to accommodate different software distribution models:
- GitHub releases (downloading specific assets from repository releases)
- Direct executable downloads from URLs
- Windows package managers (Winget, Chocolatey)
- Archive extraction with custom post-processing scripts
This flexible approach handles the diverse distribution methods used by Elite Dangerous community tools.

### User Interface Design
The GUI implements an Elite Dangerous-inspired dark theme with orange and blue accent colors. The interface uses a checkbox-based selection system for optional applications and provides real-time progress feedback during installations. The design prioritizes clarity and ease of use for users who may not be technically experienced.

### Build and Distribution
The application uses PyInstaller to create standalone executables, bundling all dependencies and the configuration file into a single distributable file. This approach eliminates dependency management issues for end users and ensures consistent behavior across different Windows environments.

### Error Handling and Logging
The application implements comprehensive logging to both file and console outputs, enabling troubleshooting of installation issues. Error handling focuses on graceful degradation, allowing partial installations to succeed even if individual components fail.

## External Dependencies

### Core Python Libraries
- **tkinter/tkinter.ttk**: Primary GUI framework for cross-platform desktop interface
- **requests**: HTTP client for downloading applications and accessing GitHub APIs
- **subprocess**: System integration for executing installers and running post-installation scripts
- **threading**: Asynchronous operations to prevent GUI freezing during downloads
- **zipfile**: Archive extraction capabilities for compressed software packages
- **hashlib**: File integrity verification through checksum validation

### Build and Packaging Tools
- **PyInstaller**: Converts Python application into standalone executable for distribution
- **pathlib**: Modern path handling for cross-platform file system operations

### Third-Party Software Sources
- **GitHub API**: Primary source for community-developed Elite Dangerous tools
- **Software Vendor Websites**: Direct downloads from hardware manufacturers (VIRPIL, VKB, Thrustmaster, Logitech)
- **Windows Package Managers**: Integration with Winget and Chocolatey for system-level installations

### Multi-Game Tool Ecosystem (29 Total Tools)

#### Elite Dangerous (19 Tools)
- **Game Data Tools**: ED Market Connector, EDDiscovery for market and exploration data
- **Voice and Audio**: EDDI voice response system, VoiceAttack voice control
- **Hardware Control**: Joystick Gremlin, HidHide, vJoy for input device management
- **Head Tracking**: OpenTrack, TrackIR, Tobii Game Hub for immersive head movement
- **Manufacturer Software**: VIRPIL VPC, VKB DevCfg, Thrustmaster TARGET for specific hardware brands
- **Utilities**: AutoHotkey v2, 7-Zip, EDEngineer, EDHM-UI, EDMC Overlay Plugin

#### Star Citizen (5 Web Tools)
- **SC Trade Tools**: Primary trade route optimization platform
- **Erkul DPS Calculator**: Ship loadout builder and DPS calculator
- **UEX Corporation**: Comprehensive trading, mining, and marketplace data
- **CCU Game**: Ship upgrade chain optimization and fleet planning
- **GameGlass**: Touchscreen controls for Star Citizen

#### EVE Online (5 Tools)
- **PYFA**: Python Fitting Assistant (desktop application)
- **EVE Guru**: Manufacturing planner with profitability optimization (web)
- **Ravworks**: Free market and industry tool (web)
- **Pathfinder**: Wormhole mapping and fleet management (web)
- **EVE Workbench**: Web-based fitting and market tools (web)

## Multi-Game Research & Expansion

### Star Citizen Tool Ecosystem (Research Completed 2024)

#### Trading & Economy Tools
- **SC Trade Tools** (sc-trade.tools) - Primary trade route optimization platform with mobile app
- **UEX Corp** (uexcorp.space) - Comprehensive trading, mining, and marketplace data
- **Galactic Logistics** (gallog.co) - Visual route planning with starmap integration
- **VerseMate** - Interactive trade planning with ship size filtering

#### Ship Building & Combat
- **Erkul Games** (erkul.games) - Ship loadout builder and DPS calculator (community standard)
- **Hardpoint.io** - Ship fitting comparison tool
- **Subliminal Loadouts** (subliminal.gg) - Curated ship builds for different gameplay styles
- **Spviewer** - Detailed ship comparison and analysis

#### Fleet & Organization Management
- **CCU Game** (ccugame.app) - Ship upgrade chain optimization and fleet planning
- **FleetYards.net** - Ship database and fleet management
- **MyFleet.space** - Organization fleet tracking (verification required)
- **SC Org.Tools** (scorg.tools) - Complete organizational suite with event management

#### Mobile & Specialized Apps
- **GameGlass** - iOS/Android touchscreen controls for Star Citizen
- **Star Citizen Assistant** - Mobile ship dashboard and control interface
- **VerseGuide** - Personal travel guide with planetary information
- **Universal Item Finder** - Equipment location and pricing search

#### Navigation & Resources
- **Star Citizen Wiki** (starcitizen.tools) - Comprehensive game information database
- **SnarePlan** - Quantum interdiction planning tool
- **ATMO Esports** (atmo.gg) - Competitive gaming platform for tournaments

### EVE Online Tool Ecosystem (Research Completed 2024)

#### Fitting & Ship Tools
- **PYFA** (Python Fitting Assistant) - Primary fitting tool (GitHub: pyfa-org/Pyfa)
  - Cross-platform, actively maintained replacement for deprecated EFT
  - Character skill simulation, fleet booster effects, damage pattern testing
- **EVEShip.fit** - Web-based fitting tool for sharing fits online
- **Theorycrafter** - Next-generation fitting tool (fast, ergonomic interface)
- **EVE Workbench** - Web-based fitting browsing with market integration

#### Fleet Management & Mapping
- **Pathfinder** - Wormhole mapping tool (community forks active, original discontinued)
  - MonoliYoda's Fork and Goryn-clade Fork (v2.2.4, April 2024)
  - Public instances: pathfinder.ashharrison.co.uk, pathfinder-eve.space
- **RIFT Intel Fusion Tool** - Advanced intel and mapping
- **IntelWalker** - Intel monitoring and early warning system
- **Alliance Auth** - Corporation/alliance management platform

#### Industrial & Market Tools
- **EVE Guru** (eveguru.online) - Manufacturing planner with profitability optimization (Updated Oct 2024)
- **Ravworks** (ravworks.com) - Free market and industry tool with invention analysis
- **Fuzzwork Blueprint Calculator** (fuzzwork.co.uk) - Comprehensive manufacturing suite
- **EVE Tycoon** (evetycoon.com) - Profit tracking across multiple characters
- **EVE Online Industry Calculator** - T1/T2/T3/capital manufacturing calculator

#### Specialized Applications
- **GESI** - Google Sheets ESI integration for data analysis
- **Neucore** - Alliance management with ESI proxy
- **JitaCalendar** - Fleet scheduling with ESI integration
- **EVE Buddy** - Multi-platform companion app (Windows/Linux/macOS)

#### Technical Infrastructure
- **ESI (EVE Swagger Interface)** - Official API with improved reliability in 2024
  - Rate limiting implementation, reduced 5xx errors to 1 in 10,000 requests
  - Enhanced stability with better timeout handling
- **CCP SSO Authentication** - Secure login without storing credentials