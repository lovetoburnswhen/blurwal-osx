"""
Path constants used in other modules.

Author: Benedikt Vollmerhaus
License: MIT
"""

import tempfile
from pathlib import Path

#: The cache directory to save transition frames in
CACHE_DIR = Path.home() / '.cache/blurwal'

#: The temporary directory to save comparison frames in
TEMP_DIR = Path(tempfile.gettempdir()) / 'blurwal'

#: The flat file for storing the original wallpaper's path
ORIGINAL_PATH = CACHE_DIR / 'original-path'

#: feh's background setter script with the current wallpaper
FEHBG_FILE = Path.home() / '.fehbg'
