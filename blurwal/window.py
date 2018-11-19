"""
Window and workspace operations using Xlib.

Author: Benedikt Vollmerhaus
License: MIT
"""

import logging
from typing import List

import Xlib
from ewmh import EWMH


def count_on_current_ws(ignored_classes: List[str]) -> int:
    """
    Count the number of open windows on the current workspace.

    Windows with a class in the given ignore list, bad windows,
    or ones missing a _NET_WM_DESKTOP property are not counted.

    :param ignored_classes: A list of window classes to ignore
    :return: The number of open windows on the workspace
    """
    ewmh = EWMH()
    window_count = 0

    all_windows = ewmh.getClientList()
    windows_on_workspace = [window for window in all_windows if
                            get_workspace(window) == ewmh.getCurrentDesktop()]

    for window in windows_on_workspace:
        window_class = window.get_wm_class()

        if window_class is not None and window_class[1] in ignored_classes:
            logging.info("Ignoring window with class '%s'.", window_class[1])
        else:
            window_count += 1

    return window_count


def get_workspace(window) -> int:
    """
    Return the given window's workspace number or -1 if the window
    is invalid or is missing the required _NET_WM_DESKTOP property.

    :param window: A window whose workspace number to get
    :return: The window's workspace number or -1 if missing
    """
    ewmh = EWMH()

    try:
        return ewmh.getWmDesktop(window)
    except Xlib.error.BadWindow:
        logging.info('Bad window (id: %s)', window.id)
    except TypeError:
        logging.warning('Window (id: %s) has no workspace number.', window.id)

    return -1
