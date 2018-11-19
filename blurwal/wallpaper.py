"""
Functions for retrieving and setting the wallpaper.

Author: Benedikt Vollmerhaus
License: MIT
"""

import logging
import re
import subprocess
import sys
from pathlib import Path

from blurwal import paths


def change_to(path: str) -> None:
    """
    Set the given image as the wallpaper using feh.

    :param path: The image to set as the wallpaper
    :return: None
    """
    logging.debug('Setting wallpaper to: %s', path)
    subprocess.run(['feh', '--bg-fill', path])


def changed_externally() -> bool:
    """
    Check whether the wallpaper has been changed externally.

    :return: Whether the wallpaper has been changed externally
    """
    return not is_transition() and get_current() != get_original()


def is_transition() -> bool:
    """
    Check whether the current wallpaper is a transition frame.

    :return: Whether the current wallpaper is a transition frame
    """
    current_wallpaper = Path(get_current())

    if current_wallpaper.parent.resolve() != paths.CACHE_DIR.resolve():
        return False

    return re.match(r'frame-\d+', current_wallpaper.name) is not None


def get_current() -> str:
    """
    Return the current wallpaper's path from the ~/.fehbg file.

    :return: The current wallpaper's path
    """
    try:
        wallpaper_path = re.search(r"'(.*)'", paths.FEHBG_FILE.read_text())
        if not wallpaper_path:
            logging.error('Could not extract current wallpaper from ~/.fehbg')
            sys.exit(1)

        return wallpaper_path.group(1)
    except FileNotFoundError:
        logging.exception('Could not open ~/.fehbg')
        sys.exit(1)


def get_original() -> str:
    """
    Return the original wallpaper's path from the path storage file.

    :return: The original wallpaper's path
    """
    with paths.ORIGINAL_PATH.open() as file:
        return file.readline().strip()


def set_original(path: str) -> None:
    """
    Save the given original wallpaper's path in the path storage file.

    :param path: The path to save
    :return: None
    """
    paths.ORIGINAL_PATH.write_text(path)


def restore_original() -> None:
    """
    Restore the original wallpaper.

    :return: None
    """
    try:
        original_path = get_original()
        logging.info('Restoring original wallpaper: %s', original_path)
        change_to(original_path)
    except FileNotFoundError:
        logging.error('Could not restore original wallpaper, '
                      'please set it manually.')
        sys.exit(1)
