# Exiles Installer - Developer Guide

## 🏗️ Architecture Overview

The Exiles Installer is built with a modular Python architecture using Tkinter for the GUI and a JSON-based configuration system for managing applications across multiple games.

### Core Components

```
src/main.py
├── ExilesInstaller (Main Class)
│   ├── UI Management (Tkinter widgets and layouts)
│   ├── Installation Engine (Multi-method installers)
│   ├── Configuration Management (JSON loading and validation)
│   ├── Game Switching Logic (Dynamic UI updates)
│   └── Logging System (File and GUI logging)
│
src/apps.json
├── Multi-Game Configuration
│   ├── Metadata (version, supported games)
│   ├── Game Definitions (ED, SC, EVE)
│   └── Application Catalogs (per-game tool lists)
```

## 🎮 Multi-Game Architecture

### Game Structure
```json
{
  "games": {
    "game_id": {
      "name": "Display Name",
      "description": "Game description",
      "color_theme": {
        "primary": "#color1",
        "secondary": "#color2"
      },
      "apps": [...]
    }
  }
}
```

### Application Entry Schema
```json
{
  "id": "unique_identifier",
  "name": "Display Name",
  "install_type": "github|exe|web|winget|chocolatey|zip",
  "description": "What this tool does",
  "optional": true|false,
  "category": "Tool Category",
  
  // Type-specific fields
  "url": "direct_download_url",
  "github_repo": "owner/repo",
  "github_asset": "asset_filename",
  "winget_id": "package.id",
  "checksum": "sha256_hash",
  
  // Post-installation
  "post_steps": [
    {
      "Name": "Step Name",
      "Script": "PowerShell command"
    }
  ]
}
```

## 🔧 Installation Methods

### 1. GitHub Releases (`install_type: "github"`)
```python
def install_via_github(self, app):
    # Fetches latest release from GitHub API
    # Downloads specific asset file
    # Supports checksum verification
```

**Configuration Example:**
```json
{
  "install_type": "github",
  "github_repo": "EDCD/EDMarketConnector",
  "github_asset": "EDMarketConnector_Setup.exe"
}
```

### 2. Direct Downloads (`install_type: "exe"`)
```python
def download_and_install(self, url, filename, app):
    # Streams large downloads efficiently
    # Optional SHA-256 checksum validation
    # Handles various file types
```

### 3. Web Tools (`install_type: "web"`)
```python
def install_via_web(self, app):
    # Opens URL in default browser
    # Displays prominent bookmark reminders
    # Returns immediately (no download)
```

### 4. Package Managers (`install_type: "winget|chocolatey"`)
```python
def install_via_package_manager(self, app):
    # Uses Windows Package Manager (winget)
    # Falls back to Chocolatey if specified
    # Handles package manager errors gracefully
```

### 5. Archive Extraction (`install_type: "zip"`)
```python
def install_via_zip(self, app):
    # Downloads and extracts ZIP files
    # Supports post-extraction scripts
    # Validates archive integrity
```

## 🎨 UI Architecture

### Main Window Structure
```
Root Window (1200x800)
├── Header Frame
│   ├── Title Label
│   └── Game Selection Dropdown
├── Filter Frame
│   ├── Search Entry
│   └── Category Filter
├── Apps Frame (Scrollable)
│   └── App Cards (Dynamic)
├── Control Frame
│   ├── Install Button
│   └── Settings Button
└── Progress Frame
    ├── Progress Bar
    ├── Status Label
    └── Log Text Widget
```

### App Card Component
```python
def create_app_card(self, app, app_icons):
    """
    Creates visual card with:
    - Checkbox for selection
    - App icon (emoji-based)
    - Name and description
    - Optional/Required badge
    - Status indicator
    - Hover effects
    """
```

### Game Switching Logic
```python
def on_game_change(self, selected_game_name):
    """
    Handles game selection changes:
    1. Map display name to game ID
    2. Update current_game property
    3. Clear existing selections
    4. Refresh UI with new app list
    """
```

## 📝 Configuration Management

### Settings System
```python
class ExilesInstaller:
    def load_settings(self):
        # Loads from exiles_config.json
        # Provides defaults for missing values
        # Validates setting types and ranges
    
    def save_settings(self):
        # Persists user preferences
        # Maintains JSON formatting
        # Handles write errors gracefully
```

### Default Settings
```json
{
  "download_directory": "~/Downloads/ExilesHUD",
  "download_timeout": 300,
  "max_concurrent_downloads": 3,
  "auto_scroll_log": true,
  "log_level": "info"
}
```

## 🔍 Logging System

### Multi-Level Logging
```python
def log_message(self, message, level="info"):
    """
    Supports multiple log levels:
    - info: General information (blue)
    - success: Successful operations (green) 
    - warning: Non-fatal issues (orange)
    - error: Failures requiring attention (red)
    """
```

### Log Destinations
1. **GUI Text Widget**: Real-time feedback with color coding
2. **File System**: Persistent logs for troubleshooting
3. **Console**: Debug output during development

## 🧪 Testing Strategy

### Unit Tests
```python
# build/test_installer.py
def test_github_releases():
    # Tests GitHub API integration
    # Validates asset filtering logic
    
def test_multi_game_switching():
    # Verifies game selection changes
    # Ensures UI updates correctly
```

### Integration Tests
```python
def test_installation_workflow():
    # End-to-end installation testing
    # Validates logging and error handling
    
def test_web_tools():
    # Tests browser integration
    # Validates bookmark reminders
```

## 🏗️ Build System
### Preferred Local Build (scripts)

PowerShell:
. .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python .\scripts\link_doctor.py --fix
pytest -q           # or: pytest -q --runslow
python .\scripts\build_onedir.py
pwsh .\scripts\make_installer_inno.ps1

Artifacts (output):
- artifacts\ExilesInstaller-portable-<version>.zip
- artifacts\ExilesInstaller-<version>-Setup.exe
- artifacts\SHA256SUMS.txt (optional; can be generated in the script)

Tip: You can still build with the spec directly for debugging PyInstaller behavior, but the scripts are the canonical path for release artifacts.

```powershell
. .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python .\scripts\link_doctor.py --fix
pytest -q           # or: pytest -q --runslow
python .\scripts\build_onedir.py
pwsh .\scripts\make_installer_inno.ps1
```
### PyInstaller Configuration
The build scripts wrap these options (reference):

- Mode: onedir (folder with ExilesInstaller.exe)
- GUI: --windowed
- Icon: installer\icons\exiles.ico
- Hidden imports: tkinter, tkinter.ttk, tkinter.messagebox, tkinter.filedialog, requests, webbrowser
- Tcl/Tk data: --collect-data tcl and --collect-data tk

Equivalent CLI (reference only):
python -m PyInstaller --noconfirm --onedir --windowed ^
  --name ExilesInstaller ^
  --icon installer\icons\exiles.ico ^
  --clean ^
  --collect-data tcl --collect-data tk ^
  --hidden-import tkinter --hidden-import tkinter.ttk ^
  --hidden-import tkinter.messagebox --hidden-import tkinter.filedialog ^
  --hidden-import requests --hidden-import webbrowser ^
  src\main.py
```python
# ExilesInstaller.spec (args for reference)
pyinstaller_args = [
    "--onefile",                    # Single executable
    "--windowed",                   # No console window
    "--name=ExilesInstaller",       # Output filename
    "--add-data=src/apps.json:.",   # Include JSON config
    "--hidden-import=tkinter.ttk",  # Ensure GUI components
    "--hidden-import=requests",     # HTTP client
    "--hidden-import=webbrowser",   # Browser integration
    "--clean",                      # Fresh build
    "src/main.py"                   # Entry point
]
```

### Build Automation
```python
def build_executable():
    """
    Automated build process:
    1. Check system requirements
    2. Install PyInstaller if needed
    3. Clean previous builds
    4. Execute PyInstaller with options
    5. Validate output and report size
    """
```

## 🔧 Adding New Games

### Step 1: Update JSON Configuration
```json
{
  "games": {
    "new_game_id": {
      "name": "New Game",
      "description": "Game description",
      "color_theme": {
        "primary": "#color1",
        "secondary": "#color2"
      },
      "apps": [
        // Add game-specific tools
      ]
    }
  }
}
```

### Step 2: Add Game Icons (Optional)
```python
# In populate_app_cards method
app_icons = {
    'NewTool': '🎮',  # Add emoji icon
    # ...existing icons
}
```

### Step 3: Update Documentation
- Add game to README.md
- Include in USER_GUIDE.md
- Update tool counts and descriptions

## 🔧 Adding New Tools

### Supported Installation Types
1. **GitHub Release**: `install_type: "github"`
2. **Direct Download**: `install_type: "exe"`
3. **Web Tool**: `install_type: "web"`
4. **Package Manager**: `install_type: "winget"`
5. **Archive**: `install_type: "zip"`

### Example: Adding a GitHub Tool
```json
{
  "id": "new_tool",
  "name": "New Tool Name",
  "install_type": "github",
  "github_repo": "owner/repository",
  "github_asset": "installer.exe",
  "optional": true,
  "description": "What this tool does for players",
  "category": "Tool Category"
}
```

### Example: Adding a Web Tool
```json
{
  "id": "new_web_tool",
  "name": "Web Tool Name", 
  "install_type": "web",
  "url": "https://tool-website.com",
  "optional": false,
  "description": "Browser-based tool description",
  "category": "Web Tools"
}
```

## 🔐 Security Considerations

### Download Security
- **Checksum Validation**: SHA-256 verification for critical downloads
- **HTTPS Only**: All downloads use secure connections
- **Stream Processing**: Large files handled without loading into memory
- **Temporary Storage**: Downloads cleaned up after installation

### PowerShell Execution
- **Limited Scope**: Only for configured post-installation steps
- **No User Input**: Scripts are predefined in configuration
- **Error Handling**: Failures don't crash the installer
- **Logging**: All script execution is logged

### User Permissions
- **No Elevation Required**: Most tools install in user space
- **Graceful Fallback**: Admin-required tools show clear error messages
- **Isolated Execution**: Each installation is independent

## 📊 Performance Optimization

### Download Management
```python
# Streaming downloads for large files
with requests.get(url, stream=True) as response:
    for chunk in response.iter_content(chunk_size=8192):
        # Process chunk without loading entire file
```

### UI Responsiveness
```python
# Threading for long-running operations
def start_installation_thread(self):
    thread = threading.Thread(target=self.install_selected_apps)
    thread.daemon = True
    thread.start()
```

### Memory Management
- **Generator-based Processing**: Large data streams
- **Immediate Cleanup**: Temporary files removed after use
- **Lazy Loading**: UI elements created on demand

## 🐛 Debugging

### Log Analysis
```python
# Enable debug logging
self.settings['log_level'] = 'debug'

# Custom log messages
self.log_message(f"Debug: {variable_value}", "info")
```

### Common Debugging Scenarios
1. **Installation Failures**: Check network connectivity and permissions
2. **UI Issues**: Verify Tkinter initialization and widget hierarchy
3. **Configuration Errors**: Validate JSON syntax and required fields
4. **Performance Problems**: Profile download speeds and memory usage

### Development Environment
```bash
# Install development dependencies
pip install -r requirements.txt

# Run with debug output
python src/main.py --debug

# Test specific functionality
python build/test_installer.py
```

## 🚀 Deployment

### Release Process
1. **Update Version**: Increment version in apps.json metadata
2. **Test Build**: Run `python build_release.py`
3. **Validate Functionality**: Test on clean Windows system
4. **Package Release**: Include README and release notes
5. **Distribute**: Upload to release platforms

### Replit Deployment
```python
# Configure for cloud demonstration
deploy_config_tool(
    deployment_target="vm",
    run=["python", "src/main.py"]
)
```

---

## 🤝 Contributing

### Code Style
- Follow PEP 8 conventions
- Use descriptive variable names
- Add docstrings to all methods
- Keep methods focused and small

### Pull Request Process
1. **Fork and Branch**: Create feature branch from main
2. **Test Changes**: Verify functionality across all games
3. **Update Documentation**: Include relevant docs updates
4. **Submit PR**: Provide clear description of changes

### Adding New Installation Types
If you need a new installation method:

1. **Add Method**: Implement `install_via_newtype(self, app)`
2. **Update Router**: Add case to installation type switch
3. **Test Integration**: Ensure error handling and logging
4. **Document**: Add to this developer guide

*Happy coding! Remember to test with all three game ecosystems.*