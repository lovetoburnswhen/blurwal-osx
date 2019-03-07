import logging
from typing import List

import subprocess


def count_on_current_ws(ignored_classes: List[str], ewmh: EWMH) -> int:
    """
    Count the number of open windows on the current workspace.

    Windows with a class in the given ignore list, bad windows,
    or ones missing a _NET_WM_DESKTOP property are not counted.

    :param ignored_classes: A list of window classes to ignore
    :param ewmh: An instance of EWMH for workspace retrieval
    :return: The number of open windows on the workspace
    """
    window_count = subprocess.run('''osascript -e \'
                        tell application "System Events"
                            set win_count to {}
                            repeat with theProcess in (application processes where visible is true)
                                set win_count to win_count & (value of (first attribute whose name is "AXWindows") of theProcess)
                            end repeat
                            get count of win_count
                        end tell\'''', stdout=subprocess.PIPE).stdout.decode('utf-8')

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
