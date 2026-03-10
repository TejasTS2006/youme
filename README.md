# YouTube Music Player

A Python desktop application that allows users to search YouTube, stream/play songs, download audio as MP3, and manage playlists — all from a clean modern GUI.

## Features

- 🔍 **Search YouTube** - Find songs and videos with instant results
- ▶️ **Stream & Play** - Play audio directly from YouTube
- ⬇️ **Download MP3** - Save songs as high-quality MP3 files
- 📚 **Playlist Management** - Create, edit, and manage custom playlists
- 🎵 **Playback Controls** - Play, pause, stop, next, previous with volume control
- 🌙 **Dark Theme** - Modern dark-themed interface

## Tech Stack

- **Python 3.10+**
- **yt-dlp** - YouTube search, streaming, and downloading
- **pygame** - Audio playback
- **customtkinter** - Modern dark-themed GUI
- **FFmpeg** - Audio conversion to MP3 (system dependency)

## Installation

### Prerequisites

1. **Python 3.10+** - [Download Python](https://www.python.org/downloads/)
2. **FFmpeg** - Required for audio conversion

#### Installing FFmpeg

**Windows:**
1. Download from [ffmpeg.org](https://ffmpeg.org/download.html)
2. Extract to a folder (e.g., `C:\ffmpeg`)
3. Add the `bin` folder to your PATH environment variable

**macOS:**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

### Setup the Application

1. **Clone or download** the project files
2. **Navigate** to the project directory:
   ```bash
   cd youtube_player
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Application

```bash
python main.py
```

### Application Interface

The application has three main sections:

#### 1. **Search Tab**
- Enter a search query and press Enter or click Search
- Results show song title and duration
- Each result has three buttons:
  - **▶ Play** - Stream and play the song immediately
  - **⬇ DL** - Download without playing
  - **+ Playlist** - Add to an existing playlist

#### 2. **Playlists**
- Click **"+ New Playlist"** to create a playlist
- Click any playlist name to view its contents
- In playlist view:
  - **▶ Play All** - Play all songs in sequence
  - **▶ Play** - Play individual song
  - **🗑 Remove** - Remove song from playlist

#### 3. **Downloads**
- View all downloaded MP3 files
- Shows file name and size
- **▶ Play** - Play downloaded file
- **🗑 Delete** - Remove file from disk

#### 4. **Player Controls**
- **Now Playing** - Shows current song title
- **⏮ Previous** - Play previous song in queue
- **▶/⏸ Play/Pause** - Toggle playback
- **⏹ Stop** - Stop playback
- **⏭ Next** - Play next song in queue
- **Volume Slider** - Adjust volume (0.0-1.0)
- **Status** - Shows download progress and errors

## Project Structure

```
youtube_player/
├── main.py               # Entry point
├── player.py             # Audio playback engine (pygame wrapper)
├── youtube.py            # yt-dlp: search + download logic
├── playlist_manager.py   # Playlist CRUD + persistence (JSON)
├── ui/
│   ├── app.py            # Main CTk window + layout
│   ├── search_view.py    # Search bar + results list
│   ├── playlist_view.py  # Playlist detail view
│   ├── downloads_view.py # Downloaded files view
│   └── player_bar.py     # Bottom playback controls bar
├── downloads/            # Auto-created; stores downloaded MP3s
├── playlists.json        # Auto-created; persisted playlist data
└── requirements.txt
```

## Data Storage

- **Downloaded songs** are stored in the `downloads/` folder as MP3 files
- **Playlists** are saved in `playlists.json` in the project directory
- Both are created automatically when first used

## Troubleshooting

### Common Issues

1. **"FFmpeg not found"**
   - Make sure FFmpeg is installed and in your PATH
   - Test by running `ffmpeg -version` in terminal

2. **"No sound"**
   - Check system volume
   - Ensure pygame can access audio hardware
   - Try restarting the application

3. **"Download failed"**
   - Check internet connection
   - Some YouTube videos may be region-restricted
   - Try a different search query

4. **"Application won't start"**
   - Ensure all dependencies are installed: `pip install -r requirements.txt`
   - Check Python version: `python --version` (should be 3.10+)

### Performance Tips

- Downloaded songs play faster than streaming
- Large playlists may take a moment to load
- Search results are limited to 8 items for better performance

## License

This project is for educational and personal use only. Please respect YouTube's Terms of Service and copyright laws.

## Contributing

Feel free to submit issues and enhancement requests!
