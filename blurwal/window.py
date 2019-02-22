"""
Window and workspace operations using Xlib.

Author: Benedikt Vollmerhaus
License: MIT
"""

import logging
from typing import List

import Xlib
from ewmh import EWMH


def count_on_current_ws(ignored_classes: List[str], ewmh: EWMH) -> int:
    """
    Count the number of open windows on the current workspace.

    Windows with a class in the given ignore list, bad windows,
    or ones missing a _NET_WM_DESKTOP property are not counted.

    :param ignored_classes: A list of window classes to ignore
    :param ewmh: An instance of EWMH for workspace retrieval
    :return: The number of open windows on the workspace
    """
    window_count = 0

    all_windows = ewmh.getClientList()
    windows_on_ws = [w for w in all_windows
                     if get_workspace(w, ewmh) == ewmh.getCurrentDesktop()]

    for window in windows_on_ws:
        try:
            window_class = window.get_wm_class()
        except Xlib.error.BadWindow:
            logging.info('Ignoring bad window (id: %s)', window.id)
            continue

        if window_class is not None and window_class[1] in ignored_classes:
            logging.info("Ignoring window with class '%s'.", window_class[1])
            continue

        window_count += 1

    return window_count


def get_workspace(window, ewmh: EWMH) -> int:
    """
    Return the given window's workspace number or -1 if the window
    is invalid or is missing the required _NET_WM_DESKTOP property.

    :param window: A window whose workspace number to get
    :param ewmh: An instance of EWMH for workspace retrieval
    :return: The window's workspace number or -1 if missing
    """
    try:
        return ewmh.getWmDesktop(window)
    except Xlib.error.BadWindow:
        logging.info('Bad window (id: %s)', window.id)
    except TypeError:
        logging.warning('Window (id: %s) has no workspace number.', window.id)

    return -1
