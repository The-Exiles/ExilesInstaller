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
        self.root.geometry("1280x900")
        self.root.configure(bg='#0a0e13')
        self.root.minsize(1000, 700)
        
        # Modern Exiles brand color scheme
        self.colors = {
            'bg_primary': '#0a0e13',       # Deep space black
            'bg_secondary': '#12181f',     # Card backgrounds
            'bg_panel': '#1a2028',         # Input/widget backgrounds
            'bg_accent': '#232b34',        # Subtle accent backgrounds
            'bg_hover': '#2a3441',         # Hover states
            'accent_primary': '#e53e3e',   # Modern red (more vibrant)
            'accent_secondary': '#c53030', # Darker red accent
            'accent_tertiary': '#9c1c1c',  # Deep red for hover states
            'accent_glow': '#ff6b6b',      # Bright red for emphasis
            'text_primary': '#f7fafc',     # Pure white text
            'text_secondary': '#e2e8f0',   # Light gray text
            'text_muted': '#a0aec0',       # Muted text
            'border': '#2d3748',           # Subtle borders
            'border_accent': '#4a5568',    # Emphasized borders
            'success': '#38a169',          # Modern green
            'warning': '#ed8936',          # Modern orange
            'error': '#e53e3e',            # Modern red
            'info': '#3182ce'              # Modern blue
        }
        
        # Modern typography system
        self.fonts = {
            'heading': ('Segoe UI', 24, 'bold'),       # Large headings
            'subheading': ('Segoe UI', 18, 'bold'),    # Section headings  
            'ui_large': ('Segoe UI', 14, 'bold'),      # Large UI elements
            'ui_medium': ('Segoe UI', 12, 'normal'),   # Standard UI elements
            'ui_small': ('Segoe UI', 10, 'normal'),    # Small UI elements
            'body': ('Segoe UI', 11, 'normal'),        # Body text
            'monospace': ('Consolas', 10, 'normal'),   # Code/log text
            'button': ('Segoe UI', 12, 'bold'),        # Button text
            'caption': ('Segoe UI', 9, 'normal')       # Small captions
        }
        
        # Load apps configuration
        self.apps_config = self.load_apps_config()
        self.selected_apps = set()
        self.installation_progress = {}
        
        # Load settings from config file
        self.settings = self.load_settings()
        
        # Update checking configuration - Exiles Downloads site
        base_url = self.settings.get('update_server', 'https://downloads.exiles.one').rstrip('/')
        self.update_config = {
            'check_url': f'{base_url}/api/installer/version',
            'download_url': f'{base_url}/api/installer/download',
            'apps_url': f'{base_url}/api/apps.json',
            'current_version': '1.0.0'
        }
        
        self.setup_ui()
        
        # Check for updates on startup if enabled
        if self.settings.get('auto_check_updates', True):
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
        """Setup a visually rich, modern interface"""
        # Configure window for sleek look
        self.root.configure(bg=self.colors['bg_primary'])
        
        # Create visual background gradient effect
        self.create_background_canvas()
        
        # Main container with sophisticated layout
        main_frame = tk.Frame(self.root, bg=self.colors['bg_primary'])
        main_frame.pack(fill='both', expand=True, padx=0, pady=0)
        
        # Create visual header with graphics
        self.create_visual_header(main_frame)
        
        # Main content with visual cards
        content_frame = tk.Frame(main_frame, bg=self.colors['bg_primary'])
        content_frame.pack(side='top', fill='both', expand=True, padx=30, pady=(20, 10))
        
        # Create visual dashboard layout
        self.create_visual_dashboard(content_frame)
        
        # Create visual control dock
        self.create_visual_control_dock(main_frame)
        
    def create_background_canvas(self):
        """Create a visual background with gradient effect"""
        # Canvas for background effects
        self.bg_canvas = tk.Canvas(
            self.root, 
            bg=self.colors['bg_primary'],
            highlightthickness=0
        )
        self.bg_canvas.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Add subtle grid pattern
        self.create_grid_pattern()
        
    def create_grid_pattern(self):
        """Create a subtle grid pattern background"""
        width = 1280
        height = 900
        grid_size = 40
        
        # Draw vertical lines
        for x in range(0, width, grid_size):
            self.bg_canvas.create_line(
                x, 0, x, height,
                fill=self.colors['border'], 
                width=1,
                stipple='gray25'
            )
            
        # Draw horizontal lines
        for y in range(0, height, grid_size):
            self.bg_canvas.create_line(
                0, y, width, y,
                fill=self.colors['border'], 
                width=1,
                stipple='gray25'
            )
    
    def create_visual_header(self, parent):
        """Create a visually rich header with graphics"""
        # Header with visual depth
        header_frame = tk.Frame(parent, bg=self.colors['bg_primary'], height=140)
        header_frame.pack(fill='x', pady=(20, 30))
        header_frame.pack_propagate(False)
        
        # Visual header background
        header_bg = tk.Frame(header_frame, bg=self.colors['bg_secondary'], height=120)
        header_bg.pack(fill='x', padx=20, pady=10)
        header_bg.pack_propagate(False)
        
        # Create visual elements
        self.create_header_graphics(header_bg)
        
        # Title with visual styling
        title_container = tk.Frame(header_bg, bg=self.colors['bg_secondary'])
        title_container.pack(expand=True, fill='both')
        
        # Visual brand elements
        brand_frame = tk.Frame(title_container, bg=self.colors['bg_secondary'])
        brand_frame.pack(pady=20)
        
        # Logo-style text with visual elements
        logo_frame = tk.Frame(brand_frame, bg=self.colors['bg_secondary'])
        logo_frame.pack()
        
        # Left visual accent
        left_accent = tk.Label(
            logo_frame,
            text="▣",
            font=('Segoe UI Symbol', 20),
            fg=self.colors['accent_primary'],
            bg=self.colors['bg_secondary']
        )
        left_accent.pack(side='left', padx=(0, 15))
        
        # Main title
        title_label = tk.Label(
            logo_frame,
            text="EXILES INSTALLER",
            font=('Segoe UI', 28, 'bold'),
            fg=self.colors['accent_glow'],
            bg=self.colors['bg_secondary']
        )
        title_label.pack(side='left')
        
        # Right visual accent
        right_accent = tk.Label(
            logo_frame,
            text="▣",
            font=('Segoe UI Symbol', 20),
            fg=self.colors['accent_primary'],
            bg=self.colors['bg_secondary']
        )
        right_accent.pack(side='left', padx=(15, 0))
        
        # Subtitle with visual elements
        subtitle_frame = tk.Frame(brand_frame, bg=self.colors['bg_secondary'])
        subtitle_frame.pack(pady=(10, 0))
        
        # Visual divider
        divider = tk.Label(
            subtitle_frame,
            text="━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
            font=('Segoe UI', 8),
            fg=self.colors['border_accent'],
            bg=self.colors['bg_secondary']
        )
        divider.pack()
        
        subtitle_label = tk.Label(
            subtitle_frame,
            text="Elite Dangerous Ecosystem • Automated Deployment System",
            font=('Segoe UI', 12),
            fg=self.colors['text_secondary'],
            bg=self.colors['bg_secondary']
        )
        subtitle_label.pack(pady=(5, 0))
        
    def create_header_graphics(self, parent):
        """Add visual graphics to header"""
        # Corner decorations
        corners_frame = tk.Frame(parent, bg=self.colors['bg_secondary'])
        corners_frame.pack(fill='x')
        
        # Top-left corner element
        tl_corner = tk.Label(
            corners_frame,
            text="┌─────",
            font=('Consolas', 10),
            fg=self.colors['accent_secondary'],
            bg=self.colors['bg_secondary']
        )
        tl_corner.pack(side='left', anchor='nw')
        
        # Top-right corner element
        tr_corner = tk.Label(
            corners_frame,
            text="─────┐",
            font=('Consolas', 10),
            fg=self.colors['accent_secondary'],
            bg=self.colors['bg_secondary']
        )
        tr_corner.pack(side='right', anchor='ne')
        
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
        
        # Visual quick selection presets
        self.create_visual_quick_selection(left_frame)
    
    def create_visual_dashboard(self, parent):
        """Create the main visual dashboard"""
        # Dashboard container
        dashboard = tk.Frame(parent, bg=self.colors['bg_primary'])
        dashboard.pack(fill='both', expand=True)
        
        # Create visual cards
        self.create_app_selection_card(dashboard)
        self.create_installation_monitor_card(dashboard)
        
    def create_app_selection_card(self, parent):
        """Create visually rich app selection card"""
        # Left side - App selection
        left_container = tk.Frame(parent, bg=self.colors['bg_primary'])
        left_container.pack(side='left', fill='both', expand=True, padx=(0, 15))
        
        # Card with visual styling
        card = tk.Frame(left_container, bg=self.colors['bg_secondary'])
        card.pack(fill='both', expand=True)
        
        # Card header with visual elements
        self.create_card_header(card, "⬢ APPLICATION MATRIX", "Select tools for deployment")
        
        # Visual app list
        self.create_visual_app_list(card)
        
        # Visual preset buttons
        self.create_visual_presets(card)
        
    def create_installation_monitor_card(self, parent):
        """Create visually rich installation monitor"""
        # Right side - Installation monitor
        right_container = tk.Frame(parent, bg=self.colors['bg_primary'])
        right_container.pack(side='right', fill='both', expand=True)
        
        # Card with visual styling
        card = tk.Frame(right_container, bg=self.colors['bg_secondary'])
        card.pack(fill='both', expand=True)
        
        # Card header
        self.create_card_header(card, "⬢ DEPLOYMENT MONITOR", "Real-time installation status")
        
        # Visual progress display
        self.create_visual_progress_display(card)
        
    def create_card_header(self, parent, title, subtitle):
        """Create a visually rich card header"""
        header_frame = tk.Frame(parent, bg=self.colors['bg_accent'], height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        # Header content
        header_content = tk.Frame(header_frame, bg=self.colors['bg_accent'])
        header_content.pack(expand=True, fill='both', padx=25, pady=15)
        
        # Title with icon
        title_frame = tk.Frame(header_content, bg=self.colors['bg_accent'])
        title_frame.pack(anchor='w')
        
        title_label = tk.Label(
            title_frame,
            text=title,
            font=('Segoe UI', 16, 'bold'),
            fg=self.colors['accent_glow'],
            bg=self.colors['bg_accent']
        )
        title_label.pack(side='left')
        
        # Subtitle
        subtitle_label = tk.Label(
            header_content,
            text=subtitle,
            font=('Segoe UI', 10),
            fg=self.colors['text_muted'],
            bg=self.colors['bg_accent']
        )
        subtitle_label.pack(anchor='w', pady=(5, 0))
        
        # Visual separator
        separator = tk.Frame(parent, bg=self.colors['accent_primary'], height=3)
        separator.pack(fill='x')
        
    def create_visual_app_list(self, parent):
        """Create a modern visual app cards interface"""
        # List container with visual styling
        list_container = tk.Frame(parent, bg=self.colors['bg_secondary'])
        list_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Search/filter section
        filter_section = tk.Frame(list_container, bg=self.colors['bg_panel'], height=50)
        filter_section.pack(fill='x', pady=(0, 15))
        filter_section.pack_propagate(False)
        
        filter_content = tk.Frame(filter_section, bg=self.colors['bg_panel'])
        filter_content.pack(expand=True, fill='both', padx=20, pady=10)
        
        # Search icon and field
        search_frame = tk.Frame(filter_content, bg=self.colors['bg_panel'])
        search_frame.pack(fill='x')
        
        search_icon = tk.Label(
            search_frame,
            text="🔍",
            font=('Segoe UI Emoji', 12),
            fg=self.colors['text_muted'],
            bg=self.colors['bg_panel']
        )
        search_icon.pack(side='left', padx=(0, 10))
        
        self.filter_var = tk.StringVar()
        search_entry = tk.Entry(
            search_frame,
            textvariable=self.filter_var,
            font=('Segoe UI', 11),
            bg=self.colors['bg_primary'],
            fg=self.colors['text_primary'],
            insertbackground=self.colors['text_primary'],
            bd=0,
            relief='flat'
        )
        search_entry.pack(fill='x', ipady=8)
        search_entry.bind('<KeyRelease>', self.filter_apps)
        
        # Modern app cards container
        apps_container = tk.Frame(list_container, bg=self.colors['bg_secondary'])
        apps_container.pack(fill='both', expand=True)
        
        # Create scrollable canvas for app cards
        self.apps_canvas = tk.Canvas(
            apps_container,
            bg=self.colors['bg_secondary'],
            highlightthickness=0,
            bd=0
        )
        
        # Scrollbar for app cards
        apps_scrollbar = tk.Scrollbar(
            apps_container,
            orient='vertical',
            command=self.apps_canvas.yview,
            bg=self.colors['bg_panel'],
            troughcolor=self.colors['bg_secondary'],
            activebackground=self.colors['accent_secondary']
        )
        
        # Scrollable frame inside canvas
        self.apps_scroll_frame = tk.Frame(self.apps_canvas, bg=self.colors['bg_secondary'])
        
        # Configure scrolling
        self.apps_canvas.configure(yscrollcommand=apps_scrollbar.set)
        self.apps_canvas_frame = self.apps_canvas.create_window(
            (0, 0), 
            window=self.apps_scroll_frame, 
            anchor='nw'
        )
        
        # Pack canvas and scrollbar
        self.apps_canvas.pack(side='left', fill='both', expand=True)
        apps_scrollbar.pack(side='right', fill='y')
        
        # Bind scroll events
        self.apps_scroll_frame.bind('<Configure>', self.on_apps_frame_configure)
        self.apps_canvas.bind('<Configure>', self.on_apps_canvas_configure)
        self.apps_canvas.bind_all('<MouseWheel>', self.on_apps_mousewheel)
        
        # Initialize app cards tracking
        self.app_cards = {}
        self.app_vars = {}
        
        # Populate app cards
        self.populate_app_cards()
    
    def populate_app_cards(self):
        """Populate the applications with modern visual cards"""
        try:
            # Clear existing cards
            for widget in self.apps_scroll_frame.winfo_children():
                widget.destroy()
            
            self.app_cards.clear()
            self.app_vars.clear()
            
            apps = self.apps_config.get('apps', [])
            
            # App icons mapping with professional symbols
            app_icons = {
                'EDMC': '◈',        # Market data connector
                'EDDI': '♪',        # Voice response system
                'VoiceAttack': '▶',  # Voice command software
                'EDDiscovery': '⊙',  # Exploration tracking
                'EDEngineer': '⚒',   # Engineering materials
                'EDHM-UI': '◐',     # HUD modifier
                'EDMC-Overlay': '▣', # Overlay plugin
                'JoystickGremlin': '◒', # Joystick configuration
                'HidHide': '◎',     # Device filter
                'vJoy': '◯',        # Virtual joystick
                'opentrack': '◉',   # Head tracking
                'TrackIR': '●',     # Head tracking hardware
                'TobiiGameHub': '◉●', # Eye tracking
                'VIRPIL-VPC': '✈',  # Flight controls
                'VKBDevCfg': '⚙',   # Configuration tool
                'TARGET': '◘',      # Programming software
                'Logitech-GHUB': '◆', # Gaming peripherals
                'AutoHotkey': '⚡',  # Automation scripts
                '7zip': '📦'        # Archive manager
            }
            
            # Apply current filter
            filter_text = self.filter_var.get().lower() if hasattr(self, 'filter_var') else ""
            
            for app in apps:
                app_name = app.get('name', 'Unknown')
                app_description = app.get('description', '')
                
                # Apply filter
                if filter_text and (filter_text not in app_name.lower() and 
                                   filter_text not in app_description.lower()):
                    continue
                
                self.create_app_card(app, app_icons)
                
        except Exception as e:
            logger.error(f"Error populating app cards: {e}")
            # Log error but don't show in progress text for initial load
    
    def create_app_card(self, app, app_icons):
        """Create a modern visual card for an application"""
        app_id = app.get('id', '')
        name = app.get('name', 'Unknown')
        description = app.get('description', 'No description available')
        optional = app.get('optional', True)
        
        # Get icon for this app
        icon = app_icons.get(name, '📦')
        
        # Card container with visual styling
        card_frame = tk.Frame(
            self.apps_scroll_frame,
            bg=self.colors['bg_accent'],
            relief='flat',
            bd=0
        )
        card_frame.pack(fill='x', padx=5, pady=3)
        
        # Card content with padding
        card_content = tk.Frame(card_frame, bg=self.colors['bg_accent'])
        card_content.pack(fill='x', padx=20, pady=15)
        
        # Left section with checkbox and icon
        left_section = tk.Frame(card_content, bg=self.colors['bg_accent'])
        left_section.pack(side='left', fill='y')
        
        # Checkbox variable - initialize with existing selection state
        var = tk.BooleanVar()
        var.set(app_id in self.selected_apps)  # Preserve existing selection
        self.app_vars[app_id] = var
        
        # Custom styled checkbox
        checkbox = tk.Checkbutton(
            left_section,
            variable=var,
            bg=self.colors['bg_accent'],
            fg=self.colors['accent_primary'],
            activebackground=self.colors['bg_accent'],
            activeforeground=self.colors['accent_glow'],
            selectcolor=self.colors['bg_primary'],
            relief='flat',
            bd=0,
            highlightthickness=0,
            command=lambda: self.on_app_selection_change()
        )
        checkbox.pack(side='left', padx=(0, 15))
        
        # App icon
        icon_label = tk.Label(
            left_section,
            text=icon,
            font=('Segoe UI Emoji', 24),
            bg=self.colors['bg_accent']
        )
        icon_label.pack(side='left', padx=(0, 20))
        
        # Center section with app details
        center_section = tk.Frame(card_content, bg=self.colors['bg_accent'])
        center_section.pack(side='left', fill='both', expand=True)
        
        # App name with visual styling
        name_frame = tk.Frame(center_section, bg=self.colors['bg_accent'])
        name_frame.pack(fill='x', anchor='w')
        
        name_label = tk.Label(
            name_frame,
            text=name,
            font=('Segoe UI', 14, 'bold'),
            fg=self.colors['text_primary'],
            bg=self.colors['bg_accent'],
            anchor='w'
        )
        name_label.pack(side='left')
        
        # Optional/Required badge
        required_badge = None
        if not optional:
            required_badge = tk.Label(
                name_frame,
                text="REQUIRED",
                font=('Segoe UI', 8, 'bold'),
                fg=self.colors['text_primary'],
                bg=self.colors['warning'],
                padx=8,
                pady=2
            )
            required_badge.pack(side='left', padx=(10, 0))
        
        # App description
        desc_label = tk.Label(
            center_section,
            text=description,
            font=('Segoe UI', 10),
            fg=self.colors['text_muted'],
            bg=self.colors['bg_accent'],
            anchor='w',
            justify='left',
            wraplength=400
        )
        desc_label.pack(fill='x', anchor='w', pady=(5, 0))
        
        # Right section with status indicator
        right_section = tk.Frame(card_content, bg=self.colors['bg_accent'])
        right_section.pack(side='right', fill='y')
        
        # Status indicator
        status_indicator = tk.Label(
            right_section,
            text="●",
            font=('Segoe UI', 16),
            fg=self.colors['success'] if optional else self.colors['warning'],
            bg=self.colors['bg_accent']
        )
        status_indicator.pack(pady=(10, 0))
        
        # Store card reference
        self.app_cards[app_id] = {
            'frame': card_frame,
            'checkbox': checkbox,
            'var': var,
            'app': app
        }
        
        # Hover effects for the entire card
        def on_enter(event):
            card_frame.configure(bg=self.colors['bg_hover'])
            card_content.configure(bg=self.colors['bg_hover'])
            left_section.configure(bg=self.colors['bg_hover'])
            center_section.configure(bg=self.colors['bg_hover'])
            right_section.configure(bg=self.colors['bg_hover'])
            name_frame.configure(bg=self.colors['bg_hover'])
            checkbox.configure(bg=self.colors['bg_hover'], activebackground=self.colors['bg_hover'])
            icon_label.configure(bg=self.colors['bg_hover'])
            name_label.configure(bg=self.colors['bg_hover'])
            desc_label.configure(bg=self.colors['bg_hover'])
            status_indicator.configure(bg=self.colors['bg_hover'])
            if not optional and required_badge is not None:
                required_badge.configure(bg=self.colors['warning'])
                
        def on_leave(event):
            card_frame.configure(bg=self.colors['bg_accent'])
            card_content.configure(bg=self.colors['bg_accent'])
            left_section.configure(bg=self.colors['bg_accent'])
            center_section.configure(bg=self.colors['bg_accent'])
            right_section.configure(bg=self.colors['bg_accent'])
            name_frame.configure(bg=self.colors['bg_accent'])
            checkbox.configure(bg=self.colors['bg_accent'], activebackground=self.colors['bg_accent'])
            icon_label.configure(bg=self.colors['bg_accent'])
            name_label.configure(bg=self.colors['bg_accent'])
            desc_label.configure(bg=self.colors['bg_accent'])
            status_indicator.configure(bg=self.colors['bg_accent'])
            if not optional and required_badge is not None:
                required_badge.configure(bg=self.colors['warning'])
        
        # Make entire card clickable to toggle selection
        def on_click(event):
            var.set(not var.get())
            self.on_app_selection_change()
        
        # Bind events to all card elements
        widgets_to_bind = [card_frame, card_content, left_section, center_section, right_section, 
                          name_frame, icon_label, name_label, desc_label, status_indicator]
        
        for widget in widgets_to_bind:
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)
            widget.bind("<Button-1>", on_click)
            widget.configure(cursor='hand2')
    
    def on_apps_frame_configure(self, event):
        """Configure scrolling region when frame changes"""
        self.apps_canvas.configure(scrollregion=self.apps_canvas.bbox("all"))
    
    def on_apps_canvas_configure(self, event):
        """Configure canvas when it's resized"""
        # Make the scroll frame width match the canvas
        canvas_width = event.width
        self.apps_canvas.itemconfig(self.apps_canvas_frame, width=canvas_width)
    
    def on_apps_mousewheel(self, event):
        """Handle mouse wheel scrolling in app list"""
        self.apps_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
    def create_visual_presets(self, parent):
        """Create visually appealing preset buttons"""
        # Presets section
        presets_section = tk.Frame(parent, bg=self.colors['bg_secondary'])
        presets_section.pack(fill='x', padx=20, pady=(0, 20))
        
        # Section header
        presets_header = tk.Frame(presets_section, bg=self.colors['bg_secondary'])
        presets_header.pack(fill='x', pady=(0, 15))
        
        header_divider = tk.Frame(presets_header, bg=self.colors['border_accent'], height=1)
        header_divider.pack(fill='x', pady=(0, 10))
        
        presets_title = tk.Label(
            presets_header,
            text="⚡ QUICK DEPLOY PRESETS",
            font=('Segoe UI', 12, 'bold'),
            fg=self.colors['accent_secondary'],
            bg=self.colors['bg_secondary']
        )
        presets_title.pack(anchor='w')
        
        # Preset buttons grid
        buttons_grid = tk.Frame(presets_section, bg=self.colors['bg_secondary'])
        buttons_grid.pack(fill='x')
        
        presets = [
            ("🎯 Essential", ["EDMC", "EDDI", "VoiceAttack"], "Core tools for commanders"),
            ("🗺️ Explorer", ["EDMC", "EDDiscovery", "opentrack"], "Exploration & tracking"),
            ("🕹️ HOTAS", ["JoystickGremlin", "HidHide", "vJoy"], "Flight control setup"),
            ("📦 Complete", "all", "Deploy everything")
        ]
        
        for i, (name, app_ids, desc) in enumerate(presets):
            self.create_preset_button(buttons_grid, name, desc, app_ids, i)
            
    def create_preset_button(self, parent, name, description, app_ids, index):
        """Create a single visual preset button"""
        # Button container
        btn_container = tk.Frame(parent, bg=self.colors['bg_secondary'])
        if index < 2:
            btn_container.pack(side='left', fill='x', expand=True, padx=(0, 10))
        else:
            btn_container.pack(side='left', fill='x', expand=True, padx=(10, 0))
        
        # Visual button with hover effects
        btn_frame = tk.Frame(btn_container, bg=self.colors['bg_accent'])
        btn_frame.pack(fill='both', pady=5)
        
        # Button content
        btn_content = tk.Frame(btn_frame, bg=self.colors['bg_accent'])
        btn_content.pack(expand=True, fill='both', padx=15, pady=12)
        
        # Button title
        btn_title = tk.Label(
            btn_content,
            text=name,
            font=('Segoe UI', 11, 'bold'),
            fg=self.colors['text_primary'],
            bg=self.colors['bg_accent'],
            cursor='hand2'
        )
        btn_title.pack()
        
        # Button description
        btn_desc = tk.Label(
            btn_content,
            text=description,
            font=('Segoe UI', 9),
            fg=self.colors['text_muted'],
            bg=self.colors['bg_accent'],
            cursor='hand2'
        )
        btn_desc.pack(pady=(2, 0))
        
        # Make entire button clickable
        def on_click(event):
            self.apply_preset(app_ids)
            
        def on_enter(event):
            btn_frame.configure(bg=self.colors['bg_hover'])
            btn_content.configure(bg=self.colors['bg_hover'])
            btn_title.configure(bg=self.colors['bg_hover'])
            btn_desc.configure(bg=self.colors['bg_hover'])
            
        def on_leave(event):
            btn_frame.configure(bg=self.colors['bg_accent'])
            btn_content.configure(bg=self.colors['bg_accent'])
            btn_title.configure(bg=self.colors['bg_accent'])
            btn_desc.configure(bg=self.colors['bg_accent'])
        
        # Bind events to all elements
        for widget in [btn_frame, btn_content, btn_title, btn_desc]:
            widget.bind("<Button-1>", on_click)
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)
            
    def create_visual_progress_display(self, parent):
        """Create a visually rich progress display"""
        # Progress container
        progress_container = tk.Frame(parent, bg=self.colors['bg_secondary'])
        progress_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Status display area
        status_area = tk.Frame(progress_container, bg=self.colors['bg_panel'])
        status_area.pack(fill='both', expand=True)
        
        # Status content
        status_content = tk.Frame(status_area, bg=self.colors['bg_panel'])
        status_content.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Progress text with visual styling
        self.progress_text = tk.Text(
            status_content,
            font=('Consolas', 10),
            bg=self.colors['bg_primary'],
            fg=self.colors['text_primary'],
            insertbackground=self.colors['text_primary'],
            state='disabled',
            wrap='word',
            bd=0,
            relief='flat'
        )
        
        # Progress scrollbar
        progress_scrollbar = tk.Scrollbar(
            status_content, 
            orient='vertical', 
            command=self.progress_text.yview,
            bg=self.colors['bg_panel'],
            troughcolor=self.colors['bg_secondary'],
            activebackground=self.colors['accent_secondary']
        )
        self.progress_text.configure(yscrollcommand=progress_scrollbar.set)
        
        self.progress_text.pack(side='left', fill='both', expand=True)
        progress_scrollbar.pack(side='right', fill='y')
        
        # Visual progress bar section
        progress_section = tk.Frame(progress_container, bg=self.colors['bg_secondary'])
        progress_section.pack(fill='x', pady=(15, 0))
        
        # Progress bar with visual styling
        progress_bg = tk.Frame(progress_section, bg=self.colors['bg_panel'], height=30)
        progress_bg.pack(fill='x')
        progress_bg.pack_propagate(False)
        
        progress_content = tk.Frame(progress_bg, bg=self.colors['bg_panel'])
        progress_content.pack(expand=True, fill='both', padx=20, pady=8)
        
        # Custom progress bar
        self.progress_bar = ttk.Progressbar(
            progress_content,
            mode='determinate',
            style='Custom.Horizontal.TProgressbar'
        )
        self.progress_bar.pack(fill='x')
        
        # Configure custom progress bar style
        style = ttk.Style()
        style.configure(
            'Custom.Horizontal.TProgressbar',
            background=self.colors['accent_primary'],
            troughcolor=self.colors['bg_accent'],
            borderwidth=0,
            lightcolor=self.colors['accent_primary'],
            darkcolor=self.colors['accent_primary']
        )
        
        # Status label
        self.status_label = tk.Label(
            progress_section,
            text="Ready for deployment",
            font=('Segoe UI', 10),
            fg=self.colors['text_secondary'],
            bg=self.colors['bg_secondary']
        )
        self.status_label.pack(pady=(10, 0))
        
    def create_visual_control_dock(self, parent):
        """Create a visual control dock"""
        # Control dock container  
        dock = tk.Frame(parent, bg=self.colors['bg_secondary'], height=100)
        dock.pack(side='bottom', fill='x', padx=20, pady=(5, 15))
        dock.pack_propagate(False)
        
        # Dock content
        dock_content = tk.Frame(dock, bg=self.colors['bg_secondary'])
        dock_content.pack(expand=True, fill='both', padx=30, pady=20)
        
        # Main action area
        action_area = tk.Frame(dock_content, bg=self.colors['bg_secondary'])
        action_area.pack(side='left', fill='y')
        
        # Primary action button with visual styling
        self.install_button = tk.Button(
            action_area,
            text="🚀 DEPLOY APPLICATIONS",
            font=('Segoe UI', 14, 'bold'),
            bg=self.colors['accent_primary'],
            fg=self.colors['text_primary'],
            activebackground=self.colors['accent_secondary'],
            activeforeground=self.colors['text_primary'],
            command=self.start_installation,
            cursor='hand2',
            relief='flat',
            bd=0,
            pady=18,
            padx=40
        )
        self.install_button.pack()
        
        # Secondary actions
        secondary_area = tk.Frame(dock_content, bg=self.colors['bg_secondary'])
        secondary_area.pack(side='left', fill='y', padx=(30, 0))
        
        secondary_buttons = [
            ("📋 Select All", self.select_all_apps),
            ("❌ Clear All", self.select_no_apps)
        ]
        
        for text, command in secondary_buttons:
            btn = tk.Button(
                secondary_area,
                text=text,
                font=('Segoe UI', 10),
                bg=self.colors['bg_accent'],
                fg=self.colors['text_primary'],
                activebackground=self.colors['bg_hover'],
                activeforeground=self.colors['text_primary'],
                command=command,
                relief='flat',
                bd=0,
                pady=12,
                padx=20,
                cursor='hand2'
            )
            btn.pack(pady=2)
            
            # Hover effects
            def on_enter(e, button=btn):
                button.configure(bg=self.colors['bg_hover'])
            def on_leave(e, button=btn):
                button.configure(bg=self.colors['bg_accent'])
            
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)
        
        # Utility tools area
        utilities_area = tk.Frame(dock_content, bg=self.colors['bg_secondary'])
        utilities_area.pack(side='right', fill='y')
        
        utility_buttons = [
            ("⚙️ Settings", self.show_settings),
            ("📋 View Log", self.show_log),
            ("🔄 Check Updates", self.manual_update_check)
        ]
        
        for text, command in utility_buttons:
            btn = tk.Button(
                utilities_area,
                text=text,
                font=('Segoe UI', 9),
                bg=self.colors['info'],
                fg=self.colors['text_primary'],
                activebackground=self.colors['bg_hover'],
                activeforeground=self.colors['text_primary'],
                command=command,
                relief='flat',
                bd=0,
                pady=8,
                padx=15,
                cursor='hand2'
            )
            btn.pack(side='left', padx=3)
            
            # Hover effects
            def on_enter(e, button=btn):
                button.configure(bg=self.colors['bg_hover'])
            def on_leave(e, button=btn):
                button.configure(bg=self.colors['info'])
            
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)
    
    def create_visual_quick_selection(self, parent):
        """This method is replaced by create_visual_presets"""
        pass
    
    def on_app_selection_change(self, event=None):
        """Handle app selection changes with card interface"""
        try:
            self.selected_apps.clear()
            
            # Get selected apps from checkboxes
            for app_id, var in self.app_vars.items():
                if var.get():
                    self.selected_apps.add(app_id)
            
            # Update status
            count = len(self.selected_apps)
            if hasattr(self, 'status_label'):
                self.status_label.configure(text=f"{count} applications selected for deployment")
                
        except Exception as e:
            logger.error(f"Error in app selection: {e}")
    
    def filter_apps(self, event=None):
        """Filter the app cards based on search text"""
        try:
            # Refresh the cards with current filter
            self.populate_app_cards()
                    
        except Exception as e:
            logger.error(f"Error filtering apps: {e}")
    
    def apply_preset(self, app_ids):
        """Apply a preset selection with card interface"""
        try:
            # Clear current selection
            for var in self.app_vars.values():
                var.set(False)
            self.selected_apps.clear()
            
            if app_ids == "all":
                # Select all visible apps
                for app_id, var in self.app_vars.items():
                    var.set(True)
                    self.selected_apps.add(app_id)
            else:
                # Select specific apps
                for app_id in app_ids:
                    if app_id in self.app_vars:
                        self.app_vars[app_id].set(True)
                        self.selected_apps.add(app_id)
            
            # Update status
            count = len(self.selected_apps)
            if hasattr(self, 'status_label'):
                self.status_label.configure(text=f"{count} applications selected for deployment")
                
        except Exception as e:
            logger.error(f"Error applying preset: {e}")
        
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
        """Legacy method - now redirects to card-based interface"""
        # This method is replaced by populate_app_cards for the new visual interface
        if hasattr(self, 'populate_app_cards'):
            self.populate_app_cards()
        else:
            logger.warning("populate_app_cards method not available - interface may not be initialized")
            
    # Removed duplicate filter_apps method - using the card-based version
        
    def select_preset(self, app_ids):
        """Select a preset group of applications - updated for card interface"""
        if app_ids == "all":
            self.select_all_apps()
            return
            
        # Clear current selection
        for var in self.app_vars.values():
            var.set(False)
        self.selected_apps.clear()
        
        # Select specified apps using card interface
        for app_id in app_ids:
            if app_id in self.app_vars:
                self.app_vars[app_id].set(True)
                self.selected_apps.add(app_id)
        
        # Update status
        self.on_app_selection_change()
                    
    def select_all_apps(self):
        """Select all applications"""
        for var in self.app_vars.values():
            var.set(True)
        self.on_app_selection_change()
        
    def select_no_apps(self):
        """Deselect all applications"""
        for var in self.app_vars.values():
            var.set(False)
        self.on_app_selection_change()
        
    def start_installation(self):
        """Start the installation process"""
        if not self.selected_apps:
            messagebox.showwarning("No Selection", "Please select at least one application to install.")
            return
            
        # Get selected apps from card interface
        selected_apps = []
        apps_list = self.apps_config.get('apps', [])
        
        for app_id in self.selected_apps:
            app_data = next((app for app in apps_list if app.get('id') == app_id), None)
            if app_data:
                selected_apps.append(app_data)
                    
        if not selected_apps:
            messagebox.showerror("Error", "No valid applications selected.")
            return
            
        # Start installation in a separate thread
        self.install_button.configure(state='disabled', text="🚀 DEPLOYING...")
        self.log_message("Starting deployment process...", "info")
        
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
            downloads_dir = Path(self.settings.get('download_directory', Path.home() / "Downloads" / "ExilesHUD"))
            downloads_dir.mkdir(parents=True, exist_ok=True)
            
            file_path = downloads_dir / filename
            
            # Download file with streaming
            self.log_message(f"Downloading from: {url}", "info")
            
            with requests.get(url, timeout=self.settings.get('download_timeout', 300), stream=True) as response:
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
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Exiles Installer Settings")
        settings_window.geometry("600x500")
        settings_window.resizable(False, False)
        settings_window.configure(bg=self.colors['bg_primary'])
        
        # Center the window
        settings_window.transient(self.root)
        settings_window.grab_set()
        
        # Main container
        main_frame = tk.Frame(settings_window, bg=self.colors['bg_primary'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(
            main_frame,
            text="◆ EXILES INSTALLER SETTINGS",
            font=self.fonts['heading'],
            fg=self.colors['accent_primary'],
            bg=self.colors['bg_primary']
        )
        title_label.pack(pady=(0, 20))
        
        # Create notebook for tabbed interface
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill='both', expand=True, pady=(0, 10))
        
        # Configure notebook style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook', background=self.colors['bg_secondary'])
        style.configure('TNotebook.Tab', background=self.colors['bg_panel'], 
                       foreground=self.colors['text_primary'], padding=[10, 5])
        style.map('TNotebook.Tab', background=[('selected', self.colors['accent_secondary'])])
        
        # General Settings Tab
        general_frame = tk.Frame(notebook, bg=self.colors['bg_secondary'])
        notebook.add(general_frame, text="General")
        self.create_general_settings(general_frame)
        
        # Downloads Tab
        downloads_frame = tk.Frame(notebook, bg=self.colors['bg_secondary'])
        notebook.add(downloads_frame, text="Downloads")
        self.create_downloads_settings(downloads_frame)
        
        # Updates Tab
        updates_frame = tk.Frame(notebook, bg=self.colors['bg_secondary'])
        notebook.add(updates_frame, text="Updates")
        self.create_updates_settings(updates_frame)
        
        # Advanced Tab
        advanced_frame = tk.Frame(notebook, bg=self.colors['bg_secondary'])
        notebook.add(advanced_frame, text="Advanced")
        self.create_advanced_settings(advanced_frame)
        
        # Button frame
        button_frame = tk.Frame(main_frame, bg=self.colors['bg_primary'])
        button_frame.pack(fill='x', pady=(10, 0))
        
        # Save and Cancel buttons
        tk.Button(
            button_frame,
            text="Save Settings",
            font=self.fonts['ui'],
            bg=self.colors['accent_primary'],
            fg=self.colors['text_primary'],
            command=lambda: self.save_settings(settings_window),
            relief='flat',
            bd=0,
            pady=8,
            padx=20
        ).pack(side='right', padx=(10, 0))
        
        tk.Button(
            button_frame,
            text="Cancel",
            font=self.fonts['ui'],
            bg=self.colors['bg_panel'],
            fg=self.colors['text_primary'],
            command=settings_window.destroy,
            relief='flat',
            bd=0,
            pady=8,
            padx=20
        ).pack(side='right')
        
        # Load current settings
        self.load_current_settings()
    
    def create_general_settings(self, parent):
        """Create general settings tab"""
        container = tk.Frame(parent, bg=self.colors['bg_secondary'])
        container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Download Directory
        dir_frame = tk.Frame(container, bg=self.colors['bg_secondary'])
        dir_frame.pack(fill='x', pady=(0, 15))
        
        tk.Label(
            dir_frame,
            text="Default Download Directory:",
            font=self.fonts['ui'],
            fg=self.colors['text_primary'],
            bg=self.colors['bg_secondary']
        ).pack(anchor='w')
        
        dir_input_frame = tk.Frame(dir_frame, bg=self.colors['bg_secondary'])
        dir_input_frame.pack(fill='x', pady=(5, 0))
        
        self.download_dir_var = tk.StringVar(value=str(Path.home() / "Downloads" / "ExilesHUD"))
        
        tk.Entry(
            dir_input_frame,
            textvariable=self.download_dir_var,
            font=self.fonts['ui_small'],
            bg=self.colors['bg_panel'],
            fg=self.colors['text_primary'],
            insertbackground=self.colors['text_primary'],
            bd=0,
            relief='flat'
        ).pack(side='left', fill='x', expand=True, ipady=5)
        
        tk.Button(
            dir_input_frame,
            text="Browse",
            font=self.fonts['ui_small'],
            bg=self.colors['accent_secondary'],
            fg=self.colors['text_primary'],
            command=self.browse_download_directory,
            relief='flat',
            bd=0,
            pady=5,
            padx=10
        ).pack(side='right', padx=(10, 0))
        
        # Installation Behavior
        install_frame = tk.Frame(container, bg=self.colors['bg_secondary'])
        install_frame.pack(fill='x', pady=(0, 15))
        
        tk.Label(
            install_frame,
            text="Installation Options:",
            font=self.fonts['ui'],
            fg=self.colors['text_primary'],
            bg=self.colors['bg_secondary']
        ).pack(anchor='w')
        
        self.run_installers_var = tk.BooleanVar(value=True)
        tk.Checkbutton(
            install_frame,
            text="Automatically run downloaded installers",
            variable=self.run_installers_var,
            font=self.fonts['ui_small'],
            fg=self.colors['text_primary'],
            bg=self.colors['bg_secondary'],
            selectcolor=self.colors['bg_panel'],
            activebackground=self.colors['bg_secondary'],
            activeforeground=self.colors['text_primary']
        ).pack(anchor='w', pady=(5, 0))
        
        self.cleanup_downloads_var = tk.BooleanVar(value=False)
        tk.Checkbutton(
            install_frame,
            text="Delete downloaded files after installation",
            variable=self.cleanup_downloads_var,
            font=self.fonts['ui_small'],
            fg=self.colors['text_primary'],
            bg=self.colors['bg_secondary'],
            selectcolor=self.colors['bg_panel'],
            activebackground=self.colors['bg_secondary'],
            activeforeground=self.colors['text_primary']
        ).pack(anchor='w', pady=(2, 0))
    
    def create_downloads_settings(self, parent):
        """Create downloads settings tab"""
        container = tk.Frame(parent, bg=self.colors['bg_secondary'])
        container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Download Performance
        perf_frame = tk.Frame(container, bg=self.colors['bg_secondary'])
        perf_frame.pack(fill='x', pady=(0, 15))
        
        tk.Label(
            perf_frame,
            text="Download Performance:",
            font=self.fonts['ui'],
            fg=self.colors['text_primary'],
            bg=self.colors['bg_secondary']
        ).pack(anchor='w')
        
        # Concurrent downloads
        concurrent_frame = tk.Frame(perf_frame, bg=self.colors['bg_secondary'])
        concurrent_frame.pack(fill='x', pady=(5, 10))
        
        tk.Label(
            concurrent_frame,
            text="Maximum concurrent downloads:",
            font=self.fonts['ui_small'],
            fg=self.colors['text_primary'],
            bg=self.colors['bg_secondary']
        ).pack(side='left')
        
        self.max_concurrent_var = tk.IntVar(value=3)
        concurrent_spinner = tk.Spinbox(
            concurrent_frame,
            from_=1,
            to=10,
            textvariable=self.max_concurrent_var,
            font=self.fonts['ui_small'],
            bg=self.colors['bg_panel'],
            fg=self.colors['text_primary'],
            insertbackground=self.colors['text_primary'],
            bd=0,
            relief='flat',
            width=5
        )
        concurrent_spinner.pack(side='right')
        
        # Timeout settings
        timeout_frame = tk.Frame(perf_frame, bg=self.colors['bg_secondary'])
        timeout_frame.pack(fill='x', pady=(0, 10))
        
        tk.Label(
            timeout_frame,
            text="Download timeout (seconds):",
            font=self.fonts['ui_small'],
            fg=self.colors['text_primary'],
            bg=self.colors['bg_secondary']
        ).pack(side='left')
        
        self.download_timeout_var = tk.IntVar(value=300)
        timeout_spinner = tk.Spinbox(
            timeout_frame,
            from_=60,
            to=1800,
            increment=30,
            textvariable=self.download_timeout_var,
            font=self.fonts['ui_small'],
            bg=self.colors['bg_panel'],
            fg=self.colors['text_primary'],
            insertbackground=self.colors['text_primary'],
            bd=0,
            relief='flat',
            width=8
        )
        timeout_spinner.pack(side='right')
        
        # Verification Options
        verify_frame = tk.Frame(container, bg=self.colors['bg_secondary'])
        verify_frame.pack(fill='x', pady=(0, 15))
        
        tk.Label(
            verify_frame,
            text="File Verification:",
            font=self.fonts['ui'],
            fg=self.colors['text_primary'],
            bg=self.colors['bg_secondary']
        ).pack(anchor='w')
        
        self.verify_checksums_var = tk.BooleanVar(value=True)
        tk.Checkbutton(
            verify_frame,
            text="Verify file checksums when available",
            variable=self.verify_checksums_var,
            font=self.fonts['ui_small'],
            fg=self.colors['text_primary'],
            bg=self.colors['bg_secondary'],
            selectcolor=self.colors['bg_panel'],
            activebackground=self.colors['bg_secondary'],
            activeforeground=self.colors['text_primary']
        ).pack(anchor='w', pady=(5, 0))
    
    def create_updates_settings(self, parent):
        """Create updates settings tab"""
        container = tk.Frame(parent, bg=self.colors['bg_secondary'])
        container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Update Check Settings
        update_frame = tk.Frame(container, bg=self.colors['bg_secondary'])
        update_frame.pack(fill='x', pady=(0, 15))
        
        tk.Label(
            update_frame,
            text="Automatic Updates:",
            font=self.fonts['ui'],
            fg=self.colors['text_primary'],
            bg=self.colors['bg_secondary']
        ).pack(anchor='w')
        
        self.auto_check_updates_var = tk.BooleanVar(value=True)
        tk.Checkbutton(
            update_frame,
            text="Check for updates on startup",
            variable=self.auto_check_updates_var,
            font=self.fonts['ui_small'],
            fg=self.colors['text_primary'],
            bg=self.colors['bg_secondary'],
            selectcolor=self.colors['bg_panel'],
            activebackground=self.colors['bg_secondary'],
            activeforeground=self.colors['text_primary']
        ).pack(anchor='w', pady=(5, 0))
        
        self.notify_updates_var = tk.BooleanVar(value=True)
        tk.Checkbutton(
            update_frame,
            text="Show notifications for available updates",
            variable=self.notify_updates_var,
            font=self.fonts['ui_small'],
            fg=self.colors['text_primary'],
            bg=self.colors['bg_secondary'],
            selectcolor=self.colors['bg_panel'],
            activebackground=self.colors['bg_secondary'],
            activeforeground=self.colors['text_primary']
        ).pack(anchor='w', pady=(2, 0))
        
        # Server Settings
        server_frame = tk.Frame(container, bg=self.colors['bg_secondary'])
        server_frame.pack(fill='x', pady=(0, 15))
        
        tk.Label(
            server_frame,
            text="Update Server:",
            font=self.fonts['ui'],
            fg=self.colors['text_primary'],
            bg=self.colors['bg_secondary']
        ).pack(anchor='w')
        
        tk.Label(
            server_frame,
            text="Server URL:",
            font=self.fonts['ui_small'],
            fg=self.colors['text_primary'],
            bg=self.colors['bg_secondary']
        ).pack(anchor='w', pady=(5, 2))
        
        self.update_server_var = tk.StringVar(value="https://downloads.exiles.one")
        tk.Entry(
            server_frame,
            textvariable=self.update_server_var,
            font=self.fonts['ui_small'],
            bg=self.colors['bg_panel'],
            fg=self.colors['text_primary'],
            insertbackground=self.colors['text_primary'],
            bd=0,
            relief='flat'
        ).pack(fill='x', pady=(0, 10), ipady=5)
    
    def create_advanced_settings(self, parent):
        """Create advanced settings tab"""
        container = tk.Frame(parent, bg=self.colors['bg_secondary'])
        container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Logging Settings
        log_frame = tk.Frame(container, bg=self.colors['bg_secondary'])
        log_frame.pack(fill='x', pady=(0, 15))
        
        tk.Label(
            log_frame,
            text="Logging:",
            font=self.fonts['ui'],
            fg=self.colors['text_primary'],
            bg=self.colors['bg_secondary']
        ).pack(anchor='w')
        
        level_frame = tk.Frame(log_frame, bg=self.colors['bg_secondary'])
        level_frame.pack(fill='x', pady=(5, 0))
        
        tk.Label(
            level_frame,
            text="Log level:",
            font=self.fonts['ui_small'],
            fg=self.colors['text_primary'],
            bg=self.colors['bg_secondary']
        ).pack(side='left')
        
        self.log_level_var = tk.StringVar(value="INFO")
        log_combo = ttk.Combobox(
            level_frame,
            textvariable=self.log_level_var,
            values=["DEBUG", "INFO", "WARNING", "ERROR"],
            font=self.fonts['ui_small'],
            state="readonly",
            width=15
        )
        log_combo.pack(side='right')
        
        # Developer Options
        dev_frame = tk.Frame(container, bg=self.colors['bg_secondary'])
        dev_frame.pack(fill='x', pady=(15, 0))
        
        tk.Label(
            dev_frame,
            text="Developer Options:",
            font=self.fonts['ui'],
            fg=self.colors['text_primary'],
            bg=self.colors['bg_secondary']
        ).pack(anchor='w')
        
        self.debug_mode_var = tk.BooleanVar(value=False)
        tk.Checkbutton(
            dev_frame,
            text="Enable debug mode",
            variable=self.debug_mode_var,
            font=self.fonts['ui_small'],
            fg=self.colors['text_primary'],
            bg=self.colors['bg_secondary'],
            selectcolor=self.colors['bg_panel'],
            activebackground=self.colors['bg_secondary'],
            activeforeground=self.colors['text_primary']
        ).pack(anchor='w', pady=(5, 0))
        
        self.dry_run_var = tk.BooleanVar(value=False)
        tk.Checkbutton(
            dev_frame,
            text="Dry run mode (download only, don't install)",
            variable=self.dry_run_var,
            font=self.fonts['ui_small'],
            fg=self.colors['text_primary'],
            bg=self.colors['bg_secondary'],
            selectcolor=self.colors['bg_panel'],
            activebackground=self.colors['bg_secondary'],
            activeforeground=self.colors['text_primary']
        ).pack(anchor='w', pady=(2, 0))
    
    def browse_download_directory(self):
        """Browse for download directory"""
        from tkinter import filedialog
        directory = filedialog.askdirectory(
            title="Select Download Directory",
            initialdir=self.download_dir_var.get()
        )
        if directory:
            self.download_dir_var.set(directory)
    
    def load_settings(self):
        """Load settings from configuration file"""
        default_settings = {
            'download_directory': str(Path.home() / "Downloads" / "ExilesHUD"),
            'run_installers': True,
            'cleanup_downloads': False,
            'max_concurrent_downloads': 3,
            'download_timeout': 300,
            'verify_checksums': True,
            'auto_check_updates': True,
            'notify_updates': True,
            'update_server': 'https://downloads.exiles.one',
            'log_level': 'INFO',
            'debug_mode': False,
            'dry_run': False
        }
        
        try:
            config_path = Path('exiles_config.json')
            if config_path.exists():
                with open(config_path, 'r') as f:
                    saved_settings = json.load(f)
                    default_settings.update(saved_settings)
                    logger.info("Settings loaded from config file")
            else:
                logger.info("Using default settings")
        except Exception as e:
            logger.warning(f"Failed to load settings: {e}, using defaults")
        
        return default_settings
    
    def load_current_settings(self):
        """Load current settings into dialog variables"""
        if hasattr(self, 'download_dir_var'):
            self.download_dir_var.set(self.settings.get('download_directory', ''))
            self.run_installers_var.set(self.settings.get('run_installers', True))
            self.cleanup_downloads_var.set(self.settings.get('cleanup_downloads', False))
            self.max_concurrent_var.set(self.settings.get('max_concurrent_downloads', 3))
            self.download_timeout_var.set(self.settings.get('download_timeout', 300))
            self.verify_checksums_var.set(self.settings.get('verify_checksums', True))
            self.auto_check_updates_var.set(self.settings.get('auto_check_updates', True))
            self.notify_updates_var.set(self.settings.get('notify_updates', True))
            self.update_server_var.set(self.settings.get('update_server', 'https://downloads.exiles.one'))
            self.log_level_var.set(self.settings.get('log_level', 'INFO'))
            self.debug_mode_var.set(self.settings.get('debug_mode', False))
            self.dry_run_var.set(self.settings.get('dry_run', False))
    
    def save_settings(self, settings_window):
        """Save settings and close dialog"""
        try:
            # Update internal configuration
            new_settings = {
                'download_directory': self.download_dir_var.get(),
                'run_installers': self.run_installers_var.get(),
                'cleanup_downloads': self.cleanup_downloads_var.get(),
                'max_concurrent_downloads': self.max_concurrent_var.get(),
                'download_timeout': self.download_timeout_var.get(),
                'verify_checksums': self.verify_checksums_var.get(),
                'auto_check_updates': self.auto_check_updates_var.get(),
                'notify_updates': self.notify_updates_var.get(),
                'update_server': self.update_server_var.get(),
                'log_level': self.log_level_var.get(),
                'debug_mode': self.debug_mode_var.get(),
                'dry_run': self.dry_run_var.get()
            }
            
            # Update internal settings
            self.settings.update(new_settings)
            
            # Update the update config with new server URL
            base_url = self.update_server_var.get().rstrip('/')
            self.update_config.update({
                'check_url': f'{base_url}/api/installer/version',
                'download_url': f'{base_url}/api/installer/download',
                'apps_url': f'{base_url}/api/apps.json'
            })
            
            # Update logging level
            log_level = getattr(logging, new_settings['log_level'], logging.INFO)
            logging.getLogger().setLevel(log_level)
            logger.setLevel(log_level)
            
            # Save to config file
            config_path = Path('exiles_config.json')
            with open(config_path, 'w') as f:
                json.dump(new_settings, f, indent=2)
            
            self.log_message("◆ Settings saved successfully", "success")
            messagebox.showinfo("Settings", "Settings saved successfully!")
            settings_window.destroy()
            
        except Exception as e:
            self.log_message(f"◆ Failed to save settings: {str(e)}", "error")
            messagebox.showerror("Error", f"Failed to save settings: {str(e)}")
        
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
                        if hasattr(os, 'startfile'):
                            os.startfile(str(log_path))  # type: ignore
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