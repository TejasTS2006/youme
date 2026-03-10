#!/usr/bin/env python3

"""
YouTube Music Player - Main Entry Point

A desktop application for searching, streaming, downloading, and managing
YouTube music with a modern GUI interface.
"""

import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from ui.app import YouTubePlayerApp


def main():
    """Main entry point for the application."""
    try:
        # Create and run the application
        app = YouTubePlayerApp()
        app.run()
    except KeyboardInterrupt:
        print("\nApplication closed by user")
        sys.exit(0)
    except Exception as e:
        print(f"Application error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
