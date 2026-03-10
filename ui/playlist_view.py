import customtkinter as ctk
from typing import Callable, List, Dict

from ..playlist_manager import playlist_manager


class PlaylistView(ctk.CTkScrollableFrame):
    def __init__(self, parent, playlist_name: str, on_play_song: Callable, on_back: Callable):
        """
        Initialize the playlist view.
        
        Args:
            parent: Parent widget
            playlist_name: Name of the playlist to display
            on_play_song: Callback to play a song
            on_back: Callback to go back to previous view
        """
        super().__init__(parent)
        
        self.playlist_name = playlist_name
        self.on_play_song = on_play_song
        self.on_back = on_back
        self.songs = []
        
        self._setup_ui()
        self._load_songs()
    
    def _setup_ui(self):
        """Setup the playlist view UI."""
        # Header frame
        header_frame = ctk.CTkFrame(self)
        header_frame.pack(fill="x", padx=10, pady=10)
        
        # Back button
        self.back_button = ctk.CTkButton(
            header_frame,
            text="← Back",
            width=80,
            command=self.on_back
        )
        self.back_button.pack(side="left", padx=10, pady=10)
        
        # Playlist title
        self.title_label = ctk.CTkLabel(
            header_frame,
            text=self.playlist_name,
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.title_label.pack(side="left", padx=10, pady=10)
        
        # Play All button
        self.play_all_button = ctk.CTkButton(
            header_frame,
            text="▶ Play All",
            width=100,
            command=self._play_all
        )
        self.play_all_button.pack(side="right", padx=10, pady=10)
        
        # Songs frame
        self.songs_frame = ctk.CTkFrame(self)
        self.songs_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Status label
        self.status_label = ctk.CTkLabel(
            self.songs_frame,
            text="Loading songs...",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        self.status_label.pack(pady=20)
    
    def _load_songs(self):
        """Load songs from the playlist."""
        self.songs = playlist_manager.get_songs(self.playlist_name)
        self._display_songs()
    
    def _display_songs(self):
        """Display songs in the playlist."""
        # Clear existing widgets
        for widget in self.songs_frame.winfo_children():
            widget.destroy()
        
        if not self.songs:
            self.status_label = ctk.CTkLabel(
                self.songs_frame,
                text="No songs in this playlist",
                font=ctk.CTkFont(size=14),
                text_color="gray"
            )
            self.status_label.pack(pady=20)
            return
        
        for i, song in enumerate(self.songs):
            self._create_song_row(song, i)
    
    def _create_song_row(self, song: Dict, index: int):
        """Create a row for a song."""
        row_frame = ctk.CTkFrame(self.songs_frame)
        row_frame.pack(fill="x", padx=5, pady=2)
        
        # Song info
        title = song.get('title', 'Unknown')
        duration = song.get('duration', '0:00')
        
        info_label = ctk.CTkLabel(
            row_frame,
            text=f"{title} [{duration}]",
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
            command=lambda s=song: self._play_clicked(s)
        )
        play_button.pack(side="left", padx=2)
        
        # Remove button
        remove_button = ctk.CTkButton(
            buttons_frame,
            text="🗑 Remove",
            width=70,
            command=lambda s=song: self._remove_clicked(s)
        )
        remove_button.pack(side="left", padx=2)
    
    def _play_clicked(self, song: Dict):
        """Handle play button click."""
        self.on_play_song(song)
    
    def _remove_clicked(self, song: Dict):
        """Handle remove button click."""
        song_id = song.get('id')
        if song_id and playlist_manager.remove_song(self.playlist_name, song_id):
            self._load_songs()  # Refresh the view
        else:
            self.status_label.configure(text="Failed to remove song", text_color="red")
    
    def _play_all(self):
        """Handle Play All button click."""
        if not self.songs:
            return
        
        # Play the first song and set up the queue
        self.on_play_song(self.songs[0], queue=self.songs[1:])
    
    def refresh(self):
        """Refresh the playlist view."""
        self._load_songs()
