#!/usr/bin/env python3
"""
Exiles Installer - Elite Dangerous Ecosystem Installer
A comprehensive installer for Elite Dangerous third-party tools and sim hardware
Created by: CMDR Watty
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import logging
import os
import sys
import threading
import subprocess
import requests
import zipfile
import tempfile
from pathlib import Path
from datetime import datetime
import webbrowser
import re
import hashlib

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('exiles_installer.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ExilesInstaller:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Exiles Installer - Elite Dangerous Ecosystem")
        self.root.geometry("1200x800")
        self.root.configure(bg='#0b0f14')
        
        # Exiles brand color scheme
        self.colors = {
            'bg_primary': '#0b0f14',      # HUD background dark
            'bg_secondary': '#0f1620',    # HUD background slightly lighter
            'bg_panel': '#1a1f2a',        # Medium dark for cards/panels
            'accent_primary': '#B01515',  # Exiles Red - primary accent
            'accent_secondary': '#17a2b8', # Cyan/teal for highlights
            'accent_gold': '#FFD700',     # Golden yellow for special content
            'accent_secondary': '#5bc0de',     # Light blue for exploration
            'text_primary': '#ffffff',    # White text
            'text_secondary': '#cccccc',  # Light grey text
            'text_muted': '#888888',      # Muted grey text
            'success': '#28A745',         # Green for success messages
            'warning': '#FFD700',         # Golden yellow for warnings
            'error': '#B01515'            # Exiles red for errors
        }
        
        # Exiles brand fonts with system fallbacks
        self.fonts = {
            'heading': ('Arial Black', 22, 'bold'),    # Primary font for titles
            'subheading': ('Arial', 16, 'bold'),       # Secondary headings
            'ui_large': ('Arial', 14, 'bold'),         # UI elements large
            'ui_medium': ('Arial', 12, 'normal'),      # UI elements medium
            'ui_small': ('Arial', 10, 'normal'),       # UI elements small
            'body': ('Arial', 11, 'normal'),           # Body text
            'monospace': ('Courier New', 10, 'normal') # Log/console text
        }
        
        # Load apps configuration
        self.apps_config = self.load_apps_config()
        self.selected_apps = set()
        self.installation_progress = {}
        
        # Update checking configuration
        self.update_config = {
            'check_url': 'https://your-squad-vps.com/api/installer/version',
            'download_url': 'https://your-squad-vps.com/api/installer/download',
            'apps_url': 'https://your-squad-vps.com/api/apps.json',
            'current_version': '1.0.0'
        }
        
        self.setup_ui()
        
        # Check for updates on startup
        self.check_for_updates_async()
        
    def load_apps_config(self):
        """Load applications configuration from apps.json"""
        try:
            with open('apps.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error("apps.json not found")
            messagebox.showerror("Error", "apps.json configuration file not found")
            return {"metadata": {}, "apps": []}
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in apps.json: {e}")
            messagebox.showerror("Error", f"Invalid JSON in apps.json: {e}")
            return {"metadata": {}, "apps": []}
            
    def setup_ui(self):
        """Setup the main user interface with modern spaceship HUD styling"""
        # Configure window for modern look
        self.root.configure(bg=self.colors['bg_primary'])
        
        # Main container with modern padding
        main_frame = tk.Frame(self.root, bg=self.colors['bg_primary'])
        main_frame.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Header with enhanced styling
        self.create_modern_header(main_frame)
        
        # Content area with enhanced panels
        content_frame = tk.Frame(main_frame, bg=self.colors['bg_primary'])
        content_frame.pack(fill='both', expand=True, pady=(15, 0))
        
        # Left panel - App selection with modern styling
        self.create_modern_app_selection_panel(content_frame)
        
        # Right panel - Installation progress with modern styling
        self.create_modern_progress_panel(content_frame)
        
        # Bottom control panel with enhanced styling
        self.create_modern_control_panel(main_frame)
        
    def create_modern_header(self, parent):
        """Create the header with clean spaceship styling"""
        # Clean header container
        header_frame = tk.Frame(parent, bg=self.colors['bg_secondary'], height=100)
        header_frame.pack(fill='x', pady=(0, 15))
        header_frame.pack_propagate(False)
        
        # Title container with better spacing
        title_container = tk.Frame(header_frame, bg=self.colors['bg_secondary'])
        title_container.pack(fill='both', expand=True)
        
        # Main title with enhanced styling
        title_label = tk.Label(
            title_container,
            text="◤ EXILES INSTALLER ◥",
            font=self.fonts['heading'],
            fg=self.colors['accent_primary'],
            bg=self.colors['bg_secondary']
        )
        title_label.pack(pady=(15, 5))
        
        # Subtitle with better typography
        subtitle_label = tk.Label(
            title_container,
            text="ELITE DANGEROUS ECOSYSTEM DEPLOYMENT SYSTEM",
            font=self.fonts['ui_medium'],
            fg=self.colors['accent_secondary'],
            bg=self.colors['bg_secondary']
        )
        subtitle_label.pack(pady=(0, 5))
        
        # Status bar with modern info display
        status_frame = tk.Frame(title_container, bg=self.colors['bg_panel'])
        status_frame.pack(fill='x', padx=20, pady=(5, 10))
        
        meta = self.apps_config.get('metadata', {})
        status_text = f"◆ DATABASE: {meta.get('updated', 'UNKNOWN')} ◆ MAINTAINER: {meta.get('maintainer', 'UNKNOWN')} ◆"
        status_label = tk.Label(
            status_frame,
            text=status_text,
            font=self.fonts['ui_small'],
            fg=self.colors['accent_gold'],
            bg=self.colors['bg_panel']
        )
        status_label.pack(pady=5)
        
    def create_modern_app_selection_panel(self, parent):
        """Create the modern application selection panel"""
        # Clean left panel
        left_frame = tk.Frame(parent, bg=self.colors['bg_panel'], width=500)
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # Panel header with modern styling
        header_frame = tk.Frame(left_frame, bg=self.colors['bg_secondary'], height=45)
        header_frame.pack(fill='x', padx=8, pady=(8, 0))
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="◢ APPLICATION SELECTION MATRIX ◣",
            font=self.fonts['ui_large'],
            fg=self.colors['accent_secondary'],
            bg=self.colors['bg_secondary']
        )
        title_label.pack(expand=True)
        
        # Filter controls
        filter_frame = tk.Frame(left_frame, bg=self.colors['bg_panel'])
        filter_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        tk.Label(
            filter_frame,
            text="Filter:",
            font=('Consolas', 10),
            fg=self.colors['text_primary'],
            bg=self.colors['bg_panel']
        ).pack(side='left')
        
        self.filter_var = tk.StringVar()
        filter_entry = tk.Entry(
            filter_frame,
            textvariable=self.filter_var,
            font=('Consolas', 10),
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_primary'],
            insertbackground=self.colors['text_primary']
        )
        filter_entry.pack(side='left', fill='x', expand=True, padx=(10, 0))
        filter_entry.bind('<KeyRelease>', self.filter_apps)
        
        # Apps list with scrollbar
        list_frame = tk.Frame(left_frame, bg=self.colors['bg_panel'])
        list_frame.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        self.apps_listbox = tk.Listbox(
            list_frame,
            font=('Consolas', 9),
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_primary'],
            selectbackground=self.colors['accent_primary'],
            selectforeground=self.colors['bg_primary'],
            activestyle='none',
            selectmode='multiple'
        )
        
        scrollbar = tk.Scrollbar(list_frame, orient='vertical', command=self.apps_listbox.yview)
        self.apps_listbox.configure(yscrollcommand=scrollbar.set)
        
        self.apps_listbox.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Populate apps list
        self.populate_apps_list()
        
        # Quick selection buttons
        self.create_quick_selection_buttons(left_frame)
        
    def create_modern_progress_panel(self, parent):
        """Create the modern installation progress panel"""
        # Clean right panel
        right_frame = tk.Frame(parent, bg=self.colors['bg_panel'], width=500)
        right_frame.pack(side='right', fill='both', expand=True, padx=(10, 0))
        
        # Panel header with modern styling
        header_frame = tk.Frame(right_frame, bg=self.colors['bg_secondary'], height=45)
        header_frame.pack(fill='x', padx=8, pady=(8, 0))
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="◢ DEPLOYMENT STATUS MONITOR ◣",
            font=self.fonts['ui_large'],
            fg=self.colors['accent_primary'],
            bg=self.colors['bg_secondary']
        )
        title_label.pack(expand=True)
        
        # Progress text area
        progress_frame = tk.Frame(right_frame, bg=self.colors['bg_panel'])
        progress_frame.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        self.progress_text = tk.Text(
            progress_frame,
            font=('Consolas', 9),
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_primary'],
            insertbackground=self.colors['text_primary'],
            state='disabled',
            wrap='word'
        )
        
        progress_scrollbar = tk.Scrollbar(progress_frame, orient='vertical', command=self.progress_text.yview)
        self.progress_text.configure(yscrollcommand=progress_scrollbar.set)
        
        self.progress_text.pack(side='left', fill='both', expand=True)
        progress_scrollbar.pack(side='right', fill='y')
        
        # Overall progress bar
        self.progress_bar = ttk.Progressbar(
            right_frame,
            mode='determinate',
            style='Accent.Horizontal.TProgressbar'
        )
        self.progress_bar.pack(fill='x', padx=10, pady=(0, 10))
        
        # Status label
        self.status_label = tk.Label(
            right_frame,
            text="Ready to install selected applications",
            font=('Consolas', 10),
            fg=self.colors['text_secondary'],
            bg=self.colors['bg_panel']
        )
        self.status_label.pack(pady=(0, 10))
        
    def create_modern_control_panel(self, parent):
        """Create the modern bottom control panel"""
        # Clean control panel
        control_frame = tk.Frame(parent, bg=self.colors['bg_secondary'], height=80)
        control_frame.pack(fill='x', pady=(20, 0))
        control_frame.pack_propagate(False)
        
        # Clean install button
        self.install_button = tk.Button(
            control_frame,
            text="◤ EXECUTE DEPLOYMENT ◥",
            font=self.fonts['ui_large'],
            bg=self.colors['accent_primary'],
            fg=self.colors['text_primary'],
            activebackground=self.colors['accent_secondary'],
            activeforeground=self.colors['text_primary'],
            command=self.start_installation,
            cursor='hand2',
            relief='flat',
            bd=0,
            pady=12,
            padx=20
        )
        self.install_button.pack(side='left', padx=20, pady=20)
        
        # Additional controls
        tk.Button(
            control_frame,
            text="Select All",
            font=('Consolas', 10),
            bg=self.colors['bg_panel'],
            fg=self.colors['text_primary'],
            command=self.select_all_apps
        ).pack(side='left', padx=(0, 10), pady=20)
        
        tk.Button(
            control_frame,
            text="Select None",
            font=('Consolas', 10),
            bg=self.colors['bg_panel'],
            fg=self.colors['text_primary'],
            command=self.select_no_apps
        ).pack(side='left', padx=(0, 10), pady=20)
        
        # Settings and info buttons on the right
        tk.Button(
            control_frame,
            text="Settings",
            font=('Consolas', 10),
            bg=self.colors['bg_panel'],
            fg=self.colors['text_primary'],
            command=self.show_settings
        ).pack(side='right', padx=20, pady=20)
        
        tk.Button(
            control_frame,
            text="View Log",
            font=self.fonts['ui_small'],
            bg=self.colors['bg_panel'],
            fg=self.colors['text_primary'],
            command=self.show_log,
            relief='flat',
            bd=0,
            pady=8
        ).pack(side='right', padx=(0, 10), pady=20)
        
        tk.Button(
            control_frame,
            text="◆ Check Updates",
            font=self.fonts['ui_small'],
            bg=self.colors['accent_secondary'],
            fg=self.colors['text_primary'],
            command=self.manual_update_check,
            relief='flat',
            bd=0,
            pady=8
        ).pack(side='right', padx=(0, 10), pady=20)
        
    def create_quick_selection_buttons(self, parent):
        """Create quick selection preset buttons"""
        preset_frame = tk.Frame(parent, bg=self.colors['bg_panel'])
        preset_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        tk.Label(
            preset_frame,
            text="Quick Presets:",
            font=('Consolas', 10, 'bold'),
            fg=self.colors['text_primary'],
            bg=self.colors['bg_panel']
        ).pack(anchor='w', pady=(0, 5))
        
        buttons_frame = tk.Frame(preset_frame, bg=self.colors['bg_panel'])
        buttons_frame.pack(fill='x')
        
        presets = [
            ("Essential", ["EDMC", "EDDI", "VoiceAttack", "7zip"]),
            ("Explorer", ["EDMC", "EDDiscovery", "opentrack", "AutoHotkey"]),
            ("HOTAS", ["JoystickGremlin", "HidHide", "vJoy", "TARGET"]),
            ("Complete", "all")
        ]
        
        for name, app_ids in presets:
            btn = tk.Button(
                buttons_frame,
                text=name,
                font=('Consolas', 9),
                bg=self.colors['bg_secondary'],
                fg=self.colors['text_primary'],
                command=lambda ids=app_ids: self.select_preset(ids)
            )
            btn.pack(side='left', padx=(0, 5))
            
    def populate_apps_list(self):
        """Populate the applications list"""
        self.apps_listbox.delete(0, tk.END)
        
        filter_text = self.filter_var.get().lower() if hasattr(self, 'filter_var') else ""
        
        for app in self.apps_config.get('apps', []):
            app_name = app.get('name', 'Unknown')
            app_id = app.get('id', '')
            optional = app.get('optional', True)
            
            if filter_text and filter_text not in app_name.lower() and filter_text not in app_id.lower():
                continue
                
            # Format the display text
            status = "OPT" if optional else "REQ"
            display_text = f"[{status}] {app_name} ({app_id})"
            
            self.apps_listbox.insert(tk.END, display_text)
            
    def filter_apps(self, event=None):
        """Filter applications based on search text"""
        self.populate_apps_list()
        
    def select_preset(self, app_ids):
        """Select a preset group of applications"""
        if app_ids == "all":
            self.select_all_apps()
            return
            
        # Clear current selection
        self.apps_listbox.selection_clear(0, tk.END)
        
        # Select specified apps
        for i in range(self.apps_listbox.size()):
            item_text = self.apps_listbox.get(i)
            for app_id in app_ids:
                if f"({app_id})" in item_text:
                    self.apps_listbox.selection_set(i)
                    break
                    
    def select_all_apps(self):
        """Select all applications"""
        self.apps_listbox.selection_set(0, tk.END)
        
    def select_no_apps(self):
        """Deselect all applications"""
        self.apps_listbox.selection_clear(0, tk.END)
        
    def start_installation(self):
        """Start the installation process"""
        selected_indices = self.apps_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("No Selection", "Please select at least one application to install.")
            return
            
        # Get selected apps
        selected_apps = []
        apps_list = self.apps_config.get('apps', [])
        
        for index in selected_indices:
            item_text = self.apps_listbox.get(index)
            # Extract app ID from the display text
            match = re.search(r'\(([^)]+)\)$', item_text)
            if match:
                app_id = match.group(1)
                app_data = next((app for app in apps_list if app.get('id') == app_id), None)
                if app_data:
                    selected_apps.append(app_data)
                    
        if not selected_apps:
            messagebox.showerror("Error", "No valid applications selected.")
            return
            
        # Start installation in a separate thread
        self.install_button.configure(state='disabled', text="INSTALLING...")
        self.log_message("Starting installation process...", "info")
        
        install_thread = threading.Thread(target=self.install_apps, args=(selected_apps,))
        install_thread.daemon = True
        install_thread.start()
        
    def install_apps(self, apps):
        """Install the selected applications"""
        total_apps = len(apps)
        completed = 0
        
        try:
            for app in apps:
                app_name = app.get('name', 'Unknown')
                self.log_message(f"\n{'='*50}", "info")
                self.log_message(f"Installing: {app_name}", "info")
                self.log_message(f"{'='*50}", "info")
                
                # Update progress
                self.update_progress(completed / total_apps * 100)
                self.update_status(f"Installing {app_name}...")
                
                # Install the app
                success = self.install_single_app(app)
                
                if success:
                    self.log_message(f"✓ {app_name} installed successfully", "success")
                    completed += 1
                else:
                    self.log_message(f"✗ Failed to install {app_name}", "error")
                    
                # Update progress
                self.update_progress(completed / total_apps * 100)
                
        except Exception as e:
            self.log_message(f"Installation error: {str(e)}", "error")
            logger.exception("Installation failed")
            
        finally:
            # Re-enable install button
            self.root.after(0, self.installation_complete, completed, total_apps)
            
    def install_single_app(self, app):
        """Install a single application"""
        try:
            install_type = app.get('install_type', 'unknown')
            
            if install_type == 'winget':
                return self.install_via_winget(app)
            elif install_type == 'github':
                return self.install_via_github(app)
            elif install_type in ['exe', 'msi']:
                return self.install_via_direct_download(app)
            elif install_type == 'zip':
                return self.install_via_zip(app)
            else:
                self.log_message(f"Unknown install type: {install_type}", "error")
                return False
                
        except Exception as e:
            self.log_message(f"Error installing app: {str(e)}", "error")
            logger.exception(f"Failed to install {app.get('name', 'Unknown')}")
            return False
            
    def install_via_winget(self, app):
        """Install application via winget"""
        winget_id = app.get('winget_id')
        if not winget_id:
            self.log_message("No winget ID specified", "error")
            return False
            
        self.log_message(f"Installing via winget: {winget_id}", "info")
        
        try:
            cmd = ['winget', 'install', '--id', winget_id, '--silent', '--accept-package-agreements', '--accept-source-agreements']
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                self.log_message("Winget installation completed", "success")
                return True
            else:
                self.log_message(f"Winget installation failed: {result.stderr}", "error")
                return False
                
        except subprocess.TimeoutExpired:
            self.log_message("Winget installation timed out", "error")
            return False
        except Exception as e:
            self.log_message(f"Winget installation error: {str(e)}", "error")
            return False
            
    def install_via_github(self, app):
        """Install application from GitHub releases"""
        repo = app.get('github_repo')
        asset_name = app.get('github_asset')
        
        if not repo or not asset_name:
            self.log_message("Missing GitHub repository or asset name", "error")
            return False
            
        self.log_message(f"Downloading from GitHub: {repo}", "info")
        
        try:
            # Get latest release
            api_url = f"https://api.github.com/repos/{repo}/releases/latest"
            response = requests.get(api_url, timeout=30)
            response.raise_for_status()
            
            release_data = response.json()
            
            # Find matching asset
            download_url = None
            for asset in release_data.get('assets', []):
                if asset_name in asset.get('name', ''):
                    download_url = asset.get('browser_download_url')
                    break
                    
            if not download_url:
                self.log_message(f"Asset '{asset_name}' not found in latest release", "error")
                return False
                
            # Download the file
            return self.download_and_install(download_url, asset_name, app)
            
        except Exception as e:
            self.log_message(f"GitHub download error: {str(e)}", "error")
            return False
            
    def install_via_direct_download(self, app):
        """Install application via direct download"""
        url = app.get('url')
        filename = app.get('filename')
        
        if not url or not filename:
            self.log_message("Missing download URL or filename", "error")
            return False
            
        self.log_message(f"Downloading: {filename}", "info")
        return self.download_and_install(url, filename, app)
        
    def install_via_zip(self, app):
        """Install application from zip file with streaming download"""
        url = app.get('url')
        filename = app.get('filename')
        extract_to = app.get('extract_to', filename.replace('.zip', ''))
        
        if not url or not filename:
            self.log_message("Missing download URL or filename", "error")
            return False
            
        self.log_message(f"Downloading zip: {filename}", "info")
        
        try:
            # Download zip file with streaming
            downloads_dir = Path.home() / "Downloads" / "ExilesHUD"
            downloads_dir.mkdir(parents=True, exist_ok=True)
            
            zip_path = downloads_dir / filename
            
            with requests.get(url, timeout=30, stream=True) as response:
                response.raise_for_status()
                
                total_size = int(response.headers.get('content-length', 0))
                downloaded_size = 0
                
                # Initialize hash calculator if checksum is provided and not empty
                expected_checksum = app.get('checksum', '').strip()
                hash_calculator = hashlib.sha256() if expected_checksum else None
                if expected_checksum:
                    self.log_message(f"Will verify checksum: {expected_checksum[:16]}...", "info")
                
                with open(zip_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            downloaded_size += len(chunk)
                            
                            if hash_calculator:
                                hash_calculator.update(chunk)
                
            self.log_message(f"Downloaded zip to: {zip_path} ({downloaded_size} bytes)", "info")
            
            # Verify checksum if provided
            if expected_checksum and hash_calculator:
                calculated_checksum = hash_calculator.hexdigest()
                if calculated_checksum.lower() == expected_checksum.lower():
                    self.log_message("Zip checksum verification passed", "success")
                else:
                    self.log_message(f"Zip checksum verification failed! Expected: {expected_checksum}, Got: {calculated_checksum}", "error")
                    zip_path.unlink(missing_ok=True)
                    return False
            
            # Extract zip
            extract_path = downloads_dir / extract_to
            try:
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(extract_path)
                self.log_message(f"Extracted to: {extract_path}", "info")
            except zipfile.BadZipFile:
                self.log_message("Downloaded file is not a valid zip archive", "error")
                zip_path.unlink(missing_ok=True)
                return False
            
            # Run post-installation steps
            return self.run_post_steps(app)
            
        except requests.exceptions.RequestException as e:
            self.log_message(f"Network error during zip download: {str(e)}", "error")
            return False
        except Exception as e:
            self.log_message(f"Zip installation error: {str(e)}", "error")
            return False
            
    def download_and_install(self, url, filename, app):
        """Download and install a file with streaming and optional checksum validation"""
        try:
            # Create downloads directory
            downloads_dir = Path.home() / "Downloads" / "ExilesHUD"
            downloads_dir.mkdir(parents=True, exist_ok=True)
            
            file_path = downloads_dir / filename
            
            # Download file with streaming
            self.log_message(f"Downloading from: {url}", "info")
            
            with requests.get(url, timeout=30, stream=True) as response:
                response.raise_for_status()
                
                # Get file size if available for progress tracking
                total_size = int(response.headers.get('content-length', 0))
                downloaded_size = 0
                
                # Initialize hash calculator if checksum is provided and not empty
                expected_checksum = app.get('checksum', '').strip()
                hash_calculator = hashlib.sha256() if expected_checksum else None
                if expected_checksum:
                    self.log_message(f"Will verify checksum: {expected_checksum[:16]}...", "info")
                
                with open(file_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            downloaded_size += len(chunk)
                            
                            # Update hash
                            if hash_calculator:
                                hash_calculator.update(chunk)
                            
                            # Update progress if total size known
                            if total_size > 0:
                                progress = (downloaded_size / total_size) * 100
                                if downloaded_size % (1024 * 1024) == 0:  # Log every MB
                                    self.log_message(f"Downloaded {downloaded_size // (1024*1024)}MB of {total_size // (1024*1024)}MB ({progress:.1f}%)", "info")
                
            self.log_message(f"Download completed: {file_path} ({downloaded_size} bytes)", "info")
            
            # Verify checksum if provided
            if expected_checksum and hash_calculator:
                calculated_checksum = hash_calculator.hexdigest()
                if calculated_checksum.lower() == expected_checksum.lower():
                    self.log_message("Checksum verification passed", "success")
                else:
                    self.log_message(f"Checksum verification failed! Expected: {expected_checksum}, Got: {calculated_checksum}", "error")
                    # Delete the potentially corrupted file
                    file_path.unlink(missing_ok=True)
                    return False
            
            # Install the file
            if filename.endswith('.exe') or filename.endswith('.msi'):
                return self.run_installer(file_path, app)
            else:
                self.log_message("File downloaded successfully", "success")
                return self.run_post_steps(app)
                
        except requests.exceptions.RequestException as e:
            self.log_message(f"Network error during download: {str(e)}", "error")
            return False
        except Exception as e:
            self.log_message(f"Download error: {str(e)}", "error")
            return False
            
    def run_installer(self, file_path, app):
        """Run an executable installer"""
        try:
            self.log_message(f"Running installer: {file_path.name}", "info")
            
            if file_path.suffix.lower() == '.msi':
                cmd = ['msiexec', '/i', str(file_path), '/quiet', '/norestart']
            else:
                cmd = [str(file_path), '/S']  # Common silent install flag
                
            result = subprocess.run(cmd, timeout=600, capture_output=True, text=True)
            
            if result.returncode == 0:
                self.log_message("Installation completed successfully", "success")
                # Run post-steps only if main installation succeeded
                post_success = self.run_post_steps(app)
                return post_success
            else:
                self.log_message(f"Installation failed with exit code: {result.returncode}", "error")
                if result.stderr:
                    self.log_message(f"Installer error output: {result.stderr}", "error")
                return False
                
        except subprocess.TimeoutExpired:
            self.log_message("Installer timed out", "error")
            return False
        except Exception as e:
            self.log_message(f"Installer error: {str(e)}", "error")
            return False
    
    def check_for_updates_async(self):
        """Check for updates in background thread"""
        def check_updates():
            try:
                self.check_for_updates()
            except Exception as e:
                logger.error(f"Update check failed: {e}")
        
        # Run update check in background thread so UI doesn't freeze
        update_thread = threading.Thread(target=check_updates, daemon=True)
        update_thread.start()
    
    def check_for_updates(self):
        """Check for installer and apps updates from squad VPS"""
        try:
            self.log_message("◆ Checking for updates from squad VPS...", "info")
            
            # Check installer version
            response = requests.get(
                self.update_config['check_url'],
                timeout=10,
                headers={'User-Agent': 'ExilesInstaller/1.0.0'}
            )
            
            if response.status_code == 200:
                version_data = response.json()
                latest_version = version_data.get('version', '1.0.0')
                apps_updated = version_data.get('apps_updated', '')
                
                if latest_version != self.update_config['current_version']:
                    self.log_message(f"◆ New installer version available: {latest_version}", "warning")
                    self.prompt_installer_update(latest_version)
                
                # Check if apps database is newer
                current_apps_date = self.apps_config.get('metadata', {}).get('updated', '')
                if apps_updated and apps_updated != current_apps_date:
                    self.log_message(f"◆ Updated apps database available: {apps_updated}", "warning")
                    self.prompt_apps_update()
                
                if latest_version == self.update_config['current_version'] and apps_updated == current_apps_date:
                    self.log_message("◆ All systems up to date", "success")
            else:
                self.log_message(f"◆ Update check failed: HTTP {response.status_code}", "warning")
                
        except requests.exceptions.RequestException as e:
            self.log_message(f"◆ Cannot reach squad VPS: {str(e)}", "warning")
        except Exception as e:
            self.log_message(f"◆ Update check error: {str(e)}", "error")
    
    def prompt_installer_update(self, new_version):
        """Prompt user to update installer"""
        def update_installer():
            result = messagebox.askyesno(
                "Installer Update",
                f"New Exiles Installer version {new_version} is available!\n\n"
                "Would you like to download and install the update?"
            )
            if result:
                self.download_installer_update(new_version)
        
        # Schedule UI update for main thread
        self.root.after(0, update_installer)
    
    def prompt_apps_update(self):
        """Prompt user to update apps database"""
        def update_apps():
            result = messagebox.askyesno(
                "Apps Database Update",
                "Updated applications database is available!\n\n"
                "Would you like to download the latest apps catalog?"
            )
            if result:
                self.download_apps_update()
        
        # Schedule UI update for main thread
        self.root.after(0, update_apps)
    
    def download_installer_update(self, new_version):
        """Download and prepare installer update"""
        try:
            self.log_message(f"◆ Downloading installer update v{new_version}...", "info")
            
            # Create updates directory
            updates_dir = Path.home() / "Downloads" / "ExilesHUD" / "Updates"
            updates_dir.mkdir(parents=True, exist_ok=True)
            
            # Download new installer
            response = requests.get(
                self.update_config['download_url'],
                timeout=300,
                stream=True,
                headers={'User-Agent': 'ExilesInstaller/1.0.0'}
            )
            response.raise_for_status()
            
            installer_path = updates_dir / f"ExilesInstaller_v{new_version}.exe"
            
            with open(installer_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            self.log_message(f"◆ Update downloaded: {installer_path}", "success")
            
            # Offer to run the update
            result = messagebox.askyesno(
                "Update Ready",
                f"Installer update has been downloaded to:\n{installer_path}\n\n"
                "Would you like to run the update now?\n"
                "(This will close the current installer)"
            )
            
            if result:
                subprocess.Popen([str(installer_path)])
                self.root.destroy()
                
        except Exception as e:
            self.log_message(f"◆ Update download failed: {str(e)}", "error")
    
    def download_apps_update(self):
        """Download updated apps database"""
        try:
            self.log_message("◆ Downloading updated apps database...", "info")
            
            response = requests.get(
                self.update_config['apps_url'],
                timeout=60,
                headers={'User-Agent': 'ExilesInstaller/1.0.0'}
            )
            response.raise_for_status()
            
            # Backup current apps.json
            backup_path = Path('apps.json.backup')
            if Path('apps.json').exists():
                Path('apps.json').rename(backup_path)
            
            # Save new apps.json
            new_config = response.json()
            with open('apps.json', 'w') as f:
                json.dump(new_config, f, indent=2)
            
            # Reload configuration
            self.apps_config = new_config
            
            self.log_message("◆ Apps database updated successfully", "success")
            
            # Refresh app list in UI
            self.update_app_list()
            
            messagebox.showinfo(
                "Update Complete",
                "Apps database has been updated!\n"
                "The application list has been refreshed with the latest tools."
            )
            
        except Exception as e:
            self.log_message(f"◆ Apps update failed: {str(e)}", "error")
            # Restore backup if it exists
            backup_path = Path('apps.json.backup')
            if backup_path.exists():
                backup_path.rename('apps.json')
                self.log_message("◆ Restored previous apps database", "info")
    
    def manual_update_check(self):
        """Manually trigger update check"""
        self.log_message("◆ Manual update check requested", "info")
        self.check_for_updates_async()
    
    def update_app_list(self):
        """Refresh the application list in the UI"""
        try:
            # Clear current selection
            self.selected_apps.clear()
            
            # Reload the apps listbox if it exists
            if hasattr(self, 'apps_listbox'):
                self.apps_listbox.delete(0, tk.END)
                
                # Repopulate with updated apps
                apps = self.apps_config.get('apps', [])
                for app in apps:
                    name = app.get('name', 'Unknown')
                    optional = app.get('optional', True)
                    status = '□' if optional else '■'
                    display_text = f"{status} {name}"
                    self.apps_listbox.insert(tk.END, display_text)
                    
                    # Auto-select non-optional apps
                    if not optional:
                        self.selected_apps.add(app.get('id'))
                        
            self.log_message("◆ Application list refreshed", "info")
            
        except Exception as e:
            self.log_message(f"◆ Failed to refresh app list: {str(e)}", "error")
            
    def run_post_steps(self, app):
        """Run post-installation steps"""
        post_steps = app.get('post_steps', [])
        if not post_steps:
            return True
            
        self.log_message("Running post-installation steps...", "info")
        
        try:
            for step in post_steps:
                step_name = step.get('Name', 'Unknown')
                script = step.get('Script', '')
                
                if not script:
                    continue
                    
                self.log_message(f"Executing step: {step_name}", "info")
                
                # Run PowerShell script
                cmd = ['powershell', '-Command', script]
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
                
                if result.returncode == 0:
                    self.log_message(f"Step '{step_name}' completed", "success")
                else:
                    self.log_message(f"Step '{step_name}' failed: {result.stderr}", "warning")
                    
            return True
            
        except Exception as e:
            self.log_message(f"Post-steps error: {str(e)}", "error")
            return False
            
    def log_message(self, message, level="info"):
        """Add a message to the progress log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Color coding
        color_map = {
            "info": self.colors['text_primary'],
            "success": self.colors['success'],
            "warning": self.colors['warning'],
            "error": self.colors['error']
        }
        
        color = color_map.get(level, self.colors['text_primary'])
        formatted_message = f"[{timestamp}] {message}\n"
        
        # Thread-safe UI update
        self.root.after(0, self._update_progress_text, formatted_message, color)
        
        # Also log to file
        if level == "error":
            logger.error(message)
        elif level == "warning":
            logger.warning(message)
        else:
            logger.info(message)
            
    def _update_progress_text(self, message, color):
        """Update progress text widget (thread-safe)"""
        self.progress_text.configure(state='normal')
        self.progress_text.insert(tk.END, message)
        
        # Color the last line
        last_line_start = self.progress_text.index("end-2c linestart")
        last_line_end = self.progress_text.index("end-2c lineend")
        
        self.progress_text.tag_add(f"color_{color}", last_line_start, last_line_end)
        self.progress_text.tag_configure(f"color_{color}", foreground=color)
        
        self.progress_text.configure(state='disabled')
        self.progress_text.see(tk.END)
        
    def update_progress(self, percentage):
        """Update the progress bar (thread-safe)"""
        self.root.after(0, lambda: self.progress_bar.configure(value=percentage))
        
    def update_status(self, status):
        """Update the status label (thread-safe)"""
        self.root.after(0, lambda: self.status_label.configure(text=status))
        
    def installation_complete(self, completed, total):
        """Handle installation completion"""
        self.install_button.configure(state='normal', text="► INSTALL SELECTED")
        self.update_progress(100)
        
        if completed == total:
            self.update_status(f"Installation completed! {completed}/{total} applications installed successfully.")
            self.log_message(f"\n🎉 Installation completed! {completed}/{total} applications installed successfully.", "success")
            messagebox.showinfo("Installation Complete", f"Successfully installed {completed} out of {total} applications!")
        else:
            self.update_status(f"Installation completed with errors. {completed}/{total} applications installed.")
            self.log_message(f"\n⚠️ Installation completed with errors. {completed}/{total} applications installed.", "warning")
            messagebox.showwarning("Installation Complete", f"Installed {completed} out of {total} applications. Check the log for details.")
            
    def show_settings(self):
        """Show settings dialog"""
        messagebox.showinfo("Settings", "Settings dialog coming soon!")
        
    def show_log(self):
        """Open the log file"""
        try:
            log_path = Path('exiles_installer.log').absolute()
            if log_path.exists():
                # Cross-platform way to open file
                import platform
                system = platform.system()
                if system == "Windows":
                    try:
                        import os
                        if hasattr(os, 'startfile'):
                            os.startfile(str(log_path))
                        else:
                            subprocess.run(['notepad.exe', str(log_path)])
                    except (AttributeError, OSError):
                        subprocess.run(['notepad.exe', str(log_path)])
                elif system == "Darwin":  # macOS
                    subprocess.run(["open", str(log_path)])
                else:  # Linux and others
                    subprocess.run(["xdg-open", str(log_path)])
            else:
                messagebox.showinfo("Log", "No log file found.")
        except Exception as e:
            messagebox.showerror("Error", f"Could not open log file: {str(e)}")
            
    def run(self):
        """Start the application"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            logger.info("Application interrupted by user")
        except Exception as e:
            logger.exception("Application error")
            messagebox.showerror("Error", f"Application error: {str(e)}")

if __name__ == "__main__":
    try:
        app = ExilesInstaller()
        app.run()
    except Exception as e:
        logging.exception("Failed to start application")
        print(f"Failed to start Exiles Installer: {e}")
        sys.exit(1)