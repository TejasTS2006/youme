import yt_dlp
from pathlib import Path
from typing import List, Dict, Callable, Optional


def search_youtube(query: str, max_results: int = 8) -> List[Dict]:
    """
    Search YouTube for videos and return basic info.
    
    Args:
        query: Search query string
        max_results: Maximum number of results to return
        
    Returns:
        List of dicts with keys: title, url, id, duration
    """
    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': True,
            'default_search': f'ytsearch{max_results}',
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=False)
            
        results = []
        for entry in info.get('entries', []):
            duration = entry.get('duration', 0)
            if duration:
                duration_str = f"{duration//60}:{duration%60:02d}"
            else:
                duration_str = "Unknown"
                
            results.append({
                'title': entry.get('title', 'Unknown'),
                'url': entry.get('url', ''),
                'id': entry.get('id', ''),
                'duration': duration_str
            })
            
        return results
        
    except Exception as e:
        print(f"Search error: {e}")
        return []


def download_audio(url: str, out_dir: Path, progress_cb: Optional[Callable] = None) -> Optional[Path]:
    """
    Download audio from YouTube URL and convert to MP3.
    
    Args:
        url: YouTube video URL
        out_dir: Directory to save the downloaded file
        progress_cb: Callback function for progress updates
        
    Returns:
        Path to the downloaded MP3 file, or None if failed
    """
    try:
        out_dir.mkdir(parents=True, exist_ok=True)
        
        def progress_hook(d):
            if progress_cb and d['status'] == 'downloading':
                percent_str = d.get('_percent_str', '0.0%')
                progress_cb(percent_str.strip())
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': str(out_dir / '%(title)s.%(ext)s'),
            'progress_hooks': [progress_hook],
            'quiet': True,
            'no_warnings': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            
        # Find the downloaded MP3 file
        title = info.get('title', 'audio')
        safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
        mp3_path = out_dir / f"{safe_title}.mp3"
        
        if mp3_path.exists():
            return mp3_path
        else:
            # Try to find any MP3 file in the directory
            for file in out_dir.glob("*.mp3"):
                return file
                
    except Exception as e:
        print(f"Download error: {e}")
        return None
