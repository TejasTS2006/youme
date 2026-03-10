import customtkinter as ctk
import tkinter as tk
from pathlib import Path
from typing import Optional, List, Dict

from .search_view import SearchView
from .playlist_view import PlaylistView
from .downloads_view import DownloadsView
from .player_bar import PlayerBar

from ..playlist_manager import playlist_manager
from ..player import player


class YouTubePlayerApp(ctk.CTk):
    def __init__(self):
        """Initialize the main application."""
        super().__init__()
        
        # App state
        self.current_view = None
        self.play_queue = []
        self.queue_index = 0
        
        # Setup window
        self._setup_window()
        
        # Create UI
        self._create_ui()
        
        # Show initial view
        self._show_search_view()
    
    def _setup_window(self):
        """Setup the main window."""
        self.title("YouTube Music Player")
        self.geometry("950x680")
        self.minsize(800, 600)
        
        # Set dark mode
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
    
    def _create_ui(self):
        """Create the main UI layout."""
        # Configure grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Left sidebar
        self._create_sidebar()
        
        # Right main area
        self._create_main_area()
        
        # Bottom player bar
        self._create_player_bar()
    
    def _create_sidebar(self):
        """Create the left sidebar."""
        sidebar_frame = ctk.CTkFrame(self, width=220)
        sidebar_frame.grid(row=0, column=0, sticky="nsew", padx=(5, 5), pady=5)
        sidebar_frame.grid_propagate(False)
        
        # App title
        title_label = ctk.CTkLabel(
            sidebar_frame,
            text="YouTube Player",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title_label.pack(pady=(10, 20))
        
        # Navigation buttons
        nav_frame = ctk.CTkFrame(sidebar_frame)
        nav_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        self.search_button = ctk.CTkButton(
            nav_frame,
            text="🔍 Search",
            command=self._show_search_view,
            height=35
        )
        self.search_button.pack(fill="x", pady=2)
        
        self.downloads_button = ctk.CTkButton(
            nav_frame,
            text="⬇ Downloads",
            command=self._show_downloads_view,
            height=35
        )
        self.downloads_button.pack(fill="x", pady=2)
        
        # Playlist section
        playlist_section = ctk.CTkFrame(sidebar_frame)
        playlist_section.pack(fill="both", expand=True, padx=10, pady=(10, 10))
        
        # Playlist header
        playlist_header = ctk.CTkFrame(playlist_section)
        playlist_header.pack(fill="x", pady=(10, 5))
        
        playlist_label = ctk.CTkLabel(
            playlist_header,
            text="Playlists",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        playlist_label.pack(side="left", padx=10)
        
        new_playlist_button = ctk.CTkButton(
            playlist_header,
            text="+",
            width=30,
            command=self._create_new_playlist
        )
        new_playlist_button.pack(side="right", padx=(5, 10))
        
        # Playlist list
        self.playlist_list_frame = ctk.CTkScrollableFrame(playlist_section)
        self.playlist_list_frame.pack(fill="both", expand=True, padx=5, pady=(0, 10))
        
        self._refresh_playlist_list()
    
    def _create_main_area(self):
        """Create the right main area."""
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=(0, 5), pady=5)
    
    def _create_player_bar(self):
        """Create the bottom player bar."""
        self.player_bar = PlayerBar(
            self,
            on_next=self._play_next,
            on_prev=self._play_prev
        )
        self.player_bar.grid(row=1, column=0, columnspan=2, sticky="ew", padx=5, pady=(0, 5))
    
    def _refresh_playlist_list(self):
        """Refresh the playlist list in the sidebar."""
        # Clear existing playlist buttons
        for widget in self.playlist_list_frame.winfo_children():
            widget.destroy()
        
        playlists = playlist_manager.list_names()
        
        if not playlists:
            no_playlists_label = ctk.CTkLabel(
                self.playlist_list_frame,
                text="No playlists yet",
                font=ctk.CTkFont(size=12),
                text_color="gray"
            )
            no_playlists_label.pack(pady=10)
            return
        
        for playlist_name in playlists:
            playlist_button = ctk.CTkButton(
                self.playlist_list_frame,
                text=playlist_name,
                command=lambda name=playlist_name: self._show_playlist_view(name),
                height=30,
                anchor="w"
            )
            playlist_button.pack(fill="x", pady=2, padx=5)
    
    def _create_new_playlist(self):
        """Create a new playlist."""
        dialog = ctk.CTkInputDialog(
            text="Enter playlist name:",
            title="New Playlist"
        )
        
        name = dialog.get_input()
        if name and name.strip():
            if playlist_manager.create(name.strip()):
                self._refresh_playlist_list()
                self.player_bar.set_status(f"Created playlist: {name.strip()}")
            else:
                self.player_bar.set_status(f"Playlist '{name.strip()}' already exists")
    
    def _clear_main_area(self):
        """Clear the main area."""
        for widget in self.main_frame.winfo_children():
            widget.destroy()
    
    def _show_search_view(self):
        """Show the search view."""
        self._clear_main_area()
        self.current_view = SearchView(
            self.main_frame,
            on_play_song=self._on_play_song,
            on_download_song=self._on_download_song
        )
        self.current_view.pack(fill="both", expand=True, padx=10, pady=10)
    
    def _show_playlist_view(self, playlist_name: str):
        """Show a playlist view."""
        self._clear_main_area()
        self.current_view = PlaylistView(
            self.main_frame,
            playlist_name,
            on_play_song=self._on_play_song,
            on_back=self._show_search_view
        )
        self.current_view.pack(fill="both", expand=True, padx=10, pady=10)
    
    def _show_downloads_view(self):
        """Show the downloads view."""
        self._clear_main_area()
        self.current_view = DownloadsView(
            self.main_frame,
            on_play_file=self._on_play_file
        )
        self.current_view.pack(fill="both", expand=True, padx=10, pady=10)
    
    def _on_play_song(self, song_info: dict, queue: Optional[List[Dict]] = None):
        """Handle play song request."""
        # Set up queue if provided
        if queue is not None:
            self.play_queue = queue
            self.queue_index = 0
        
        # Play the song
        self.player_bar.play_song(song_info, stream=True)
    
    def _on_download_song(self, song_info: dict):
        """Handle download song request."""
        # Download without playing
        self.player_bar.play_song(song_info, stream=False)
        # The player_bar will handle the download but won't play
        # We need to modify this to download-only
        import threading
        from ..youtube import download_audio
        
        def download_only():
            try:
                downloads_dir = Path(__file__).parent.parent / "downloads"
                
                def progress_callback(percent):
                    self.player_bar.set_status(f"Downloading: {percent}")
                
                file_path = download_audio(
                    song_info['url'], 
                    downloads_dir, 
                    progress_callback
                )
                
                if file_path:
                    self.player_bar.set_status(f"Downloaded: {song_info['title'][:30]}...")
                else:
                    self.player_bar.set_status("Download failed")
                    
            except Exception as e:
                self.player_bar.set_status(f"Error: {str(e)[:60]}")
        
        thread = threading.Thread(target=download_only)
        thread.daemon = True
        thread.start()
    
    def _on_play_file(self, file_path: Path):
        """Handle play local file request."""
        self.player_bar._play_local_file(file_path)
    
    def _play_next(self):
        """Play the next song in the queue."""
        if self.queue_index < len(self.play_queue) - 1:
            self.queue_index += 1
            next_song = self.play_queue[self.queue_index]
            self._on_play_song(next_song)
    
    def _play_prev(self):
        """Play the previous song in the queue."""
        if self.queue_index > 0:
            self.queue_index -= 1
            prev_song = self.play_queue[self.queue_index]
            self._on_play_song(prev_song)
    
    def run(self):
        """Run the application."""
        self.mainloop()
