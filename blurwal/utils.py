"""
Utility functions not specific to a module.

Author: Benedikt Vollmerhaus
License: MIT
"""

import logging
import subprocess
from typing import Tuple


def map_range(value: float, from_range: Tuple[int, int],
              to_range: Tuple[int, int]) -> float:
    """
    Map the given value from a source range to a target range.

    Examples:
      >>> map_range(0.5, (0, 1), (0, 10))
      5.0
      >>> map_range(-2, (0, -10), (0, 1))
      0.2
      >>> map_range(4, (0, 1), (0, 10))
      40.0

    :param value: The value to convert
    :param from_range: A source range (min, max)
    :param to_range: A target range (min, max)

    :return: The value in the target range
    """
    (a_1, a_2), (b_1, b_2) = from_range, to_range
    return (value - a_1) * (b_2 - b_1) / (a_2 - a_1) + b_1


def show_notification(title: str, content: str) -> None:
    """
    Show a desktop notification with the given title and content.

    :return: None
    """
    try:
        subprocess.run(['notify-send', title, content])
    except FileNotFoundError:
        logging.info('libnotify not installed, cannot show notification.')
