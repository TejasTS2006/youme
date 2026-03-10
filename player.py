import pygame
from pathlib import Path
from typing import Optional


class AudioPlayer:
    def __init__(self):
        """Initialize the audio player."""
        pygame.mixer.init()
        self.current_file: Optional[Path] = None
        self._volume = 0.7
        
    def play(self, filepath: Path) -> bool:
        """
        Play audio file.
        
        Args:
            filepath: Path to the audio file
            
        Returns:
            True if playback started successfully, False otherwise
        """
        try:
            if not filepath.exists():
                print(f"File not found: {filepath}")
                return False
                
            pygame.mixer.music.load(str(filepath))
            pygame.mixer.music.play()
            self.current_file = filepath
            pygame.mixer.music.set_volume(self._volume)
            return True
            
        except Exception as e:
            print(f"Playback error: {e}")
            return False
    
    def pause(self) -> None:
        """Pause the current playback."""
        try:
            pygame.mixer.music.pause()
        except Exception as e:
            print(f"Pause error: {e}")
    
    def resume(self) -> None:
        """Resume the paused playback."""
        try:
            pygame.mixer.music.unpause()
        except Exception as e:
            print(f"Resume error: {e}")
    
    def stop(self) -> None:
        """Stop the current playback."""
        try:
            pygame.mixer.music.stop()
            self.current_file = None
        except Exception as e:
            print(f"Stop error: {e}")
    
    def set_volume(self, volume: float) -> None:
        """
        Set the volume (0.0 to 1.0).
        
        Args:
            volume: Volume level between 0.0 and 1.0
        """
        try:
            volume = max(0.0, min(1.0, volume))
            self._volume = volume
            pygame.mixer.music.set_volume(volume)
        except Exception as e:
            print(f"Volume error: {e}")
    
    def is_playing(self) -> bool:
        """
        Check if audio is currently playing.
        
        Returns:
            True if playing, False otherwise
        """
        try:
            return pygame.mixer.music.get_busy() != 0
        except Exception:
            return False
    
    def get_current_file(self) -> Optional[Path]:
        """
        Get the currently playing file.
        
        Returns:
            Path to current file or None if not playing
        """
        return self.current_file
    
    def get_volume(self) -> float:
        """
        Get the current volume.
        
        Returns:
            Current volume level (0.0 to 1.0)
        """
        return self._volume


# Global player instance
player = AudioPlayer()
