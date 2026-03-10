import customtkinter as ctk
from pathlib import Path
from typing import Callable, List
import os

from ..player import player


class DownloadsView(ctk.CTkScrollableFrame):
    def __init__(self, parent, on_play_file: Callable):
        """
        Initialize the downloads view.
        
        Args:
            parent: Parent widget
            on_play_file: Callback to play a local file
        """
        super().__init__(parent)
        
        self.on_play_file = on_play_file
        self.downloaded_files = []
        
        self._setup_ui()
        self._load_downloads()
    
    def _setup_ui(self):
        """Setup the downloads view UI."""
        # Header
        header_label = ctk.CTkLabel(
            self,
            text="Downloaded Songs",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        header_label.pack(pady=10)
        
        # Files frame
        self.files_frame = ctk.CTkFrame(self)
        self.files_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Status label
        self.status_label = ctk.CTkLabel(
            self.files_frame,
            text="Loading downloads...",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        self.status_label.pack(pady=20)
    
    def _load_downloads(self):
        """Load downloaded MP3 files."""
        try:
            downloads_dir = Path(__file__).parent.parent / "downloads"
            
            if not downloads_dir.exists():
                downloads_dir.mkdir(parents=True, exist_ok=True)
            
            # Get all MP3 files
            self.downloaded_files = []
            for file_path in downloads_dir.glob("*.mp3"):
                if file_path.is_file():
                    # Get file size and modification time
                    stat = file_path.stat()
                    size_mb = stat.st_size / (1024 * 1024)  # Convert to MB
                    mod_time = stat.st_mtime
                    
                    self.downloaded_files.append({
                        'path': file_path,
                        'name': file_path.stem,
                        'size_mb': round(size_mb, 2),
                        'mod_time': mod_time
                    })
            
            # Sort by modification time (newest first)
            self.downloaded_files.sort(key=lambda x: x['mod_time'], reverse=True)
            
            self._display_files()
            
        except Exception as e:
            self._show_error(f"Error loading downloads: {e}")
    
    def _display_files(self):
        """Display downloaded files."""
        # Clear existing widgets
        for widget in self.files_frame.winfo_children():
            widget.destroy()
        
        if not self.downloaded_files:
            self.status_label = ctk.CTkLabel(
                self.files_frame,
                text="No downloads yet",
                font=ctk.CTkFont(size=14),
                text_color="gray"
            )
            self.status_label.pack(pady=20)
            return
        
        for file_info in self.downloaded_files:
            self._create_file_row(file_info)
    
    def _create_file_row(self, file_info: dict):
        """Create a row for a downloaded file."""
        row_frame = ctk.CTkFrame(self.files_frame)
        row_frame.pack(fill="x", padx=5, pady=2)
        
        # File info
        name = file_info['name']
        size = file_info['size_mb']
        
        info_label = ctk.CTkLabel(
            row_frame,
            text=f"{name} ({size} MB)",
            font=ctk.CTkFont(size=12),
            anchor="w"
        )
        info_label.pack(side="left", fill="x", expand=True, padx=10, pady=8)
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(row_frame)
        buttons_frame.pack(side="right", padx=10)
        
        # Play button
        play_button = ctk.CTkButton(
            buttons_frame,
            text="▶ Play",
            width=60,
            command=lambda f=file_info: self._play_clicked(f)
        )
        play_button.pack(side="left", padx=2)
        
        # Delete button
        delete_button = ctk.CTkButton(
            buttons_frame,
            text="🗑 Delete",
            width=70,
            command=lambda f=file_info: self._delete_clicked(f)
        )
        delete_button.pack(side="left", padx=2)
    
    def _play_clicked(self, file_info: dict):
        """Handle play button click."""
        file_path = file_info['path']
        self.on_play_file(file_path)
    
    def _delete_clicked(self, file_info: dict):
        """Handle delete button click."""
        file_path = file_info['path']
        
        try:
            # Stop playback if this file is currently playing
            if player.get_current_file() == file_path:
                player.stop()
            
            # Delete the file
            file_path.unlink()
            
            # Refresh the view
            self._load_downloads()
            
        except Exception as e:
            self._show_error(f"Error deleting file: {e}")
    
    def _show_error(self, message: str):
        """Show error message."""
        # Clear existing widgets
        for widget in self.files_frame.winfo_children():
            widget.destroy()
        
        error_label = ctk.CTkLabel(
            self.files_frame,
            text=message,
            font=ctk.CTkFont(size=14),
            text_color="red"
        )
        error_label.pack(pady=20)
    
    def refresh(self):
        """Refresh the downloads view."""
        self._load_downloads()
