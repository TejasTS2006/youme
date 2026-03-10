import customtkinter as ctk
import tkinter as tk
from pathlib import Path
from typing import Optional, Callable
import threading
import time

from ..player import player
from ..youtube import download_audio


class PlayerBar(ctk.CTkFrame):
    def __init__(self, parent, on_next: Optional[Callable] = None, on_prev: Optional[Callable] = None):
        """
        Initialize the player bar.
        
        Args:
            parent: Parent widget
            on_next: Callback for next button
            on_prev: Callback for previous button
        """
        super().__init__(parent, height=80)
        
        self.on_next = on_next
        self.on_prev = on_prev
        self.current_song_title = "No song playing"
        self.download_thread = None
        self.current_downloading_file = None
        
        self._setup_ui()
        self._update_ui_loop()
    
    def _setup_ui(self):
        """Setup the player bar UI."""
        # Configure grid
        self.grid_columnconfigure(1, weight=1)
        
        # Now playing label
        self.now_playing_label = ctk.CTkLabel(
            self, 
            text=self.current_song_title,
            font=ctk.CTkFont(size=14, weight="bold"),
            wraplength=340
        )
        self.now_playing_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
        # Playback controls frame
        controls_frame = ctk.CTkFrame(self)
        controls_frame.grid(row=0, column=1, padx=20, pady=5)
        
        # Control buttons
        self.prev_button = ctk.CTkButton(
            controls_frame, 
            text="⏮", 
            width=40, 
            command=self._on_prev_clicked
        )
        self.prev_button.grid(row=0, column=0, padx=2)
        
        self.play_pause_button = ctk.CTkButton(
            controls_frame, 
            text="▶", 
            width=40, 
            command=self._toggle_play_pause
        )
        self.play_pause_button.grid(row=0, column=1, padx=2)
        
        self.stop_button = ctk.CTkButton(
            controls_frame, 
            text="⏹", 
            width=40, 
            command=self._stop_playback
        )
        self.stop_button.grid(row=0, column=2, padx=2)
        
        self.next_button = ctk.CTkButton(
            controls_frame, 
            text="⏭", 
            width=40, 
            command=self._on_next_clicked
        )
        self.next_button.grid(row=0, column=3, padx=2)
        
        # Volume slider
        self.volume_slider = ctk.CTkSlider(
            self, 
            from_=0.0, 
            to=1.0, 
            value=player.get_volume(),
            command=self._on_volume_change
        )
        self.volume_slider.grid(row=0, column=2, padx=10, pady=5, sticky="ew")
        
        # Status label
        self.status_label = ctk.CTkLabel(
            self, 
            text="", 
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.status_label.grid(row=1, column=0, columnspan=3, padx=10, pady=2, sticky="w")
    
    def _toggle_play_pause(self):
        """Toggle between play and pause."""
        if player.is_playing():
            player.pause()
            self.play_pause_button.configure(text="▶")
        else:
            player.resume()
            self.play_pause_button.configure(text="⏸")
    
    def _stop_playback(self):
        """Stop playback."""
        player.stop()
        self.play_pause_button.configure(text="▶")
        self.current_song_title = "No song playing"
        self.now_playing_label.configure(text=self.current_song_title)
    
    def _on_prev_clicked(self):
        """Handle previous button click."""
        if self.on_prev:
            self.on_prev()
    
    def _on_next_clicked(self):
        """Handle next button click."""
        if self.on_next:
            self.on_next()
    
    def _on_volume_change(self, value):
        """Handle volume slider change."""
        player.set_volume(value)
    
    def play_song(self, song_info: dict, stream: bool = True):
        """
        Play a song.
        
        Args:
            song_info: Dictionary with song info (title, url, id, duration)
            stream: If True, download and play. If False, play from local file
        """
        if stream:
            self._stream_song(song_info)
        else:
            self._play_local_file(song_info)
    
    def _stream_song(self, song_info: dict):
        """Stream a song by downloading it first."""
        if self.download_thread and self.download_thread.is_alive():
            self.set_status("Already downloading...")
            return
        
        self.current_song_title = song_info.get('title', 'Unknown')
        self.now_playing_label.configure(text=f"Preparing: {self.current_song_title}")
        
        def download_and_play():
            try:
                downloads_dir = Path(__file__).parent.parent / "downloads"
                
                def progress_callback(percent):
                    self.set_status(f"Downloading: {percent}")
                
                file_path = download_audio(
                    song_info['url'], 
                    downloads_dir, 
                    progress_callback
                )
                
                if file_path and file_path.exists():
                    self.current_downloading_file = file_path
                    self.set_status("Playing...")
                    if player.play(file_path):
                        self.now_playing_label.configure(text=f"Now playing: {self.current_song_title}")
                        self.play_pause_button.configure(text="⏸")
                    else:
                        self.set_status("Failed to play")
                else:
                    self.set_status("Download failed")
                    
            except Exception as e:
                self.set_status(f"Error: {str(e)[:60]}")
        
        self.download_thread = threading.Thread(target=download_and_play)
        self.download_thread.daemon = True
        self.download_thread.start()
    
    def _play_local_file(self, file_path: Path):
        """Play a local audio file."""
        if player.play(file_path):
            self.current_song_title = file_path.stem
            self.now_playing_label.configure(text=f"Now playing: {self.current_song_title}")
            self.play_pause_button.configure(text="⏸")
            self.set_status("")
        else:
            self.set_status("Failed to play file")
    
    def set_status(self, message: str):
        """Set the status message."""
        self.status_label.configure(text=message)
    
    def _update_ui_loop(self):
        """Update UI periodically to sync with player state."""
        if player.is_playing():
            self.play_pause_button.configure(text="⏸")
        else:
            self.play_pause_button.configure(text="▶")
        
        # Schedule next update
        self.after(500, self._update_ui_loop)
