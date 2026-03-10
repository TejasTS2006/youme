import customtkinter as ctk
import tkinter as tk
from typing import Callable, List, Dict
import threading

from ..youtube import search_youtube
from ..playlist_manager import playlist_manager


class SearchView(ctk.CTkScrollableFrame):
    def __init__(self, parent, on_play_song: Callable, on_download_song: Callable):
        """
        Initialize the search view.
        
        Args:
            parent: Parent widget
            on_play_song: Callback to play a song
            on_download_song: Callback to download a song
        """
        super().__init__(parent)
        
        self.on_play_song = on_play_song
        self.on_download_song = on_download_song
        self.search_results = []
        self.is_searching = False
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup the search view UI."""
        # Search frame
        search_frame = ctk.CTkFrame(self)
        search_frame.pack(fill="x", padx=10, pady=10)
        
        # Search entry
        self.search_entry = ctk.CTkEntry(
            search_frame, 
            placeholder_text="Search YouTube...",
            font=ctk.CTkFont(size=14)
        )
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(10, 5))
        self.search_entry.bind("<Return>", lambda e: self._perform_search())
        
        # Search button
        self.search_button = ctk.CTkButton(
            search_frame, 
            text="Search", 
            command=self._perform_search,
            width=80
        )
        self.search_button.pack(side="right", padx=(5, 10))
        
        # Results frame
        self.results_frame = ctk.CTkFrame(self)
        self.results_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Status label
        self.status_label = ctk.CTkLabel(
            self.results_frame, 
            text="Enter a search query to find songs",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        self.status_label.pack(pady=20)
    
    def _perform_search(self):
        """Perform YouTube search."""
        query = self.search_entry.get().strip()
        if not query:
            return
        
        if self.is_searching:
            return
        
        self.is_searching = True
        self.status_label.configure(text="Searching...")
        self._clear_results()
        
        def search_thread():
            try:
                results = search_youtube(query, max_results=8)
                self.after(0, lambda: self._display_results(results))
            except Exception as e:
                self.after(0, lambda: self._show_error(f"Search failed: {e}"))
            finally:
                self.after(0, lambda: setattr(self, 'is_searching', False))
        
        thread = threading.Thread(target=search_thread)
        thread.daemon = True
        thread.start()
    
    def _clear_results(self):
        """Clear search results."""
        for widget in self.results_frame.winfo_children():
            widget.destroy()
    
    def _display_results(self, results: List[Dict]):
        """Display search results."""
        self.search_results = results
        self._clear_results()
        
        if not results:
            self.status_label.configure(text="No results found")
            return
        
        self.status_label.configure(text=f"Found {len(results)} results")
        
        for i, song in enumerate(results):
            self._create_result_row(song, i)
    
    def _create_result_row(self, song: Dict, index: int):
        """Create a row for a search result."""
        row_frame = ctk.CTkFrame(self.results_frame)
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
        
        # Download button
        download_button = ctk.CTkButton(
            buttons_frame,
            text="⬇ DL",
            width=50,
            command=lambda s=song: self._download_clicked(s)
        )
        download_button.pack(side="left", padx=2)
        
        # Playlist dropdown
        playlists = playlist_manager.list_names()
        if playlists:
            playlist_var = ctk.StringVar(value="Add to...")
            playlist_menu = ctk.CTkOptionMenu(
                buttons_frame,
                values=["Add to..."] + playlists,
                variable=playlist_var,
                command=lambda val, s=song: self._add_to_playlist(val, s)
            )
            playlist_menu.pack(side="left", padx=2)
        else:
            # Show message if no playlists
            no_playlist_label = ctk.CTkLabel(
                buttons_frame,
                text="No playlists",
                font=ctk.CTkFont(size=10),
                text_color="gray"
            )
            no_playlist_label.pack(side="left", padx=2)
    
    def _play_clicked(self, song: Dict):
        """Handle play button click."""
        self.on_play_song(song)
    
    def _download_clicked(self, song: Dict):
        """Handle download button click."""
        self.on_download_song(song)
    
    def _add_to_playlist(self, playlist_name: str, song: Dict):
        """Add song to playlist."""
        if playlist_name == "Add to...":
            return
        
        if playlist_manager.add_song(playlist_name, song):
            self.status_label.configure(text=f"Added to '{playlist_name}'")
        else:
            self.status_label.configure(text=f"Failed to add to '{playlist_name}'")
    
    def _show_error(self, message: str):
        """Show error message."""
        self._clear_results()
        self.status_label.configure(text=message, text_color="red")
    
    def refresh_playlists(self):
        """Refresh playlist dropdowns."""
        if self.search_results:
            self._display_results(self.search_results)
