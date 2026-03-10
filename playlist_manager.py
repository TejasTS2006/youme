import json
from pathlib import Path
from typing import List, Dict


class PlaylistManager:
    def __init__(self, file_path: Path = None):
        """
        Initialize playlist manager.
        
        Args:
            file_path: Path to the playlists JSON file
        """
        if file_path is None:
            file_path = Path(__file__).parent / "playlists.json"
        
        self.file_path = file_path
        self.playlists = self._load_playlists()
    
    def _load_playlists(self) -> Dict:
        """Load playlists from JSON file."""
        try:
            if self.file_path.exists():
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return {}
        except Exception as e:
            print(f"Error loading playlists: {e}")
            return {}
    
    def _save_playlists(self) -> None:
        """Save playlists to JSON file."""
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(self.playlists, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving playlists: {e}")
    
    def create(self, name: str) -> bool:
        """
        Create a new playlist.
        
        Args:
            name: Playlist name
            
        Returns:
            True if created successfully, False if already exists
        """
        if name in self.playlists:
            return False
        
        self.playlists[name] = []
        self._save_playlists()
        return True
    
    def delete(self, name: str) -> bool:
        """
        Delete a playlist.
        
        Args:
            name: Playlist name
            
        Returns:
            True if deleted successfully, False if not found
        """
        if name not in self.playlists:
            return False
        
        del self.playlists[name]
        self._save_playlists()
        return True
    
    def add_song(self, playlist_name: str, song_dict: Dict) -> bool:
        """
        Add a song to a playlist.
        
        Args:
            playlist_name: Name of the playlist
            song_dict: Song info with keys: id, title, url, duration
            
        Returns:
            True if added successfully, False if playlist not found
        """
        if playlist_name not in self.playlists:
            return False
        
        # Check if song already exists
        for song in self.playlists[playlist_name]:
            if song.get('id') == song_dict.get('id'):
                return False  # Song already exists
        
        self.playlists[playlist_name].append(song_dict)
        self._save_playlists()
        return True
    
    def remove_song(self, playlist_name: str, song_id: str) -> bool:
        """
        Remove a song from a playlist.
        
        Args:
            playlist_name: Name of the playlist
            song_id: ID of the song to remove
            
        Returns:
            True if removed successfully, False if not found
        """
        if playlist_name not in self.playlists:
            return False
        
        original_length = len(self.playlists[playlist_name])
        self.playlists[playlist_name] = [
            song for song in self.playlists[playlist_name] 
            if song.get('id') != song_id
        ]
        
        if len(self.playlists[playlist_name]) < original_length:
            self._save_playlists()
            return True
        
        return False
    
    def get_songs(self, playlist_name: str) -> List[Dict]:
        """
        Get all songs from a playlist.
        
        Args:
            playlist_name: Name of the playlist
            
        Returns:
            List of song dictionaries, empty list if playlist not found
        """
        return self.playlists.get(playlist_name, []).copy()
    
    def list_names(self) -> List[str]:
        """
        Get all playlist names.
        
        Returns:
            List of playlist names
        """
        return list(self.playlists.keys())
    
    def playlist_exists(self, name: str) -> bool:
        """
        Check if a playlist exists.
        
        Args:
            name: Playlist name
            
        Returns:
            True if playlist exists, False otherwise
        """
        return name in self.playlists


# Global playlist manager instance
playlist_manager = PlaylistManager()
