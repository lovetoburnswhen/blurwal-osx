"""
Author: Benedikt Vollmerhaus
License: MIT
"""

import argparse
import logging
import multiprocessing
import re
from typing import List, Optional, Tuple

import Xlib
from Xlib import X

from blurwal import frame, paths, utils, wallpaper, window
from blurwal.transition import Transition


class Blur:
    """
    Event listener for window events with high-level blurring logic.
    """

    def __init__(self, args: argparse.Namespace) -> None:
        self.window_threshold: int = args.min
        self.transition_steps: int = args.steps
        self.max_sigma: int = args.blur
        self.ignored_classes: List[str] = args.ignore

    def listen_for_events(self) -> None:
        """
        Listen for X11 events covering window creation and movement
        between workspaces and, upon receiving such an event, count
        the number of windows on the currently focused workspace.

        If the number of open windows is equal to or above the set
        threshold, initiate a blur, otherwise an unblur transition.

        The following events are monitored and should be enough to
        cover any situation in which a blur operation is necessary:

        MapNotify is sent when windows are drawn, e.g. a window
          - is opened on the current workspace
          - is moved to the current workspace
          - is shown by switching to the workspace it's on

        UnmapNotify is sent when windows are undrawn, e.g. a window
          - on the current workspace is closed
          - is moved to a different workspace
          - is hidden by switching to a different workspace

        :return: None
        """
        # Connect to X server
        display = Xlib.display.Display()

        root_win = display.screen().root
        root_win.change_attributes(event_mask=X.SubstructureNotifyMask)

        print(':: Ready and waiting for window events...')

        blur = Transition(0, 0)
        unblur = Transition(0, 0)

        while True:
            event = display.next_event()

            if event.type in (X.MapNotify, X.UnmapNotify):
                if wallpaper.changed_externally():
                    wallpaper.set_original(wallpaper.get_current())

                    if self.frames_are_outdated():
                        self.generate_transition_frames()

                window_count = window.count_on_current_ws(self.ignored_classes)
                blur, unblur = self.init_transition(window_count, blur, unblur)

    def init_transition(self, window_count: int,
                        blur: Optional[Transition],
                        unblur: Optional[Transition]) -> Tuple:
        """
        Initiate a blur or unblur transition depending on the given
        number of windows on the current workspace, and only if the
        previously started transition was in the opposite direction.

        Transitions can only be started alternately, so an unblur
        one may only occur after a blur transition and vice versa,
        regardless of whether the previous transition is finished.

        :param window_count: The number of open windows
        :param blur: The previous blur transition or None
        :param unblur: The previous unblur transition or None
        :return: The current transition threads
        """
        # Blur
        if window_count >= self.window_threshold and unblur is not None:
            unblur.stop()
            blur = Transition(unblur.current_level, self.transition_steps)
            blur.start()
            unblur = None

        # Unblur
        if window_count < self.window_threshold and blur is not None:
            blur.stop()
            unblur = Transition(blur.current_level, 0)
            unblur.start()
            blur = None

        return blur, unblur

    def frames_are_outdated(self) -> bool:
        """
        Check whether the transition frames need to be regenerated.

        This is the case if
          a) any transition step doesn't have a corresponding frame.
          b) the existing frame of some blur level differs from the
             expected one, the reference being generated on-the-fly
             from the current wallpaper.

        :return: Whether the transition frames need to be regenerated
        """
        print(':: Validating transition frames... ', end='', flush=True)

        found_frames = [f for f in paths.CACHE_DIR.iterdir()
                        if f.is_file() and re.match(r'frame-\d+\.\w+', f.name)]
        found_levels = [int(re.search(r'\d+', file.name).group(0))
                        for file in found_frames]

        if not set(range(self.transition_steps + 1)).issubset(found_levels):
            print('\033[31mOutdated\033[0m')
            logging.info('One or more frames are missing.')
            return True

        if frame.is_outdated(1, self.transition_steps, self.max_sigma):
            print('\033[31mOutdated\033[0m')
            logging.info('Wallpaper appears to have changed.')
            return True

        print('\033[32mUp-to-date\033[0m')
        return False

    def generate_transition_frames(self) -> None:
        """
        Generate frames for the transition from the original wallpaper.

        Each frame will be blurred by an increasing blur level, so that
        setting them as the wallpaper in quick succession should result
        in a smooth-ish transition. The last frame will be blurred with
        the specified maximum blur sigma.

        :return: None
        """
        logging.info('Cache path for frames: %s', paths.CACHE_DIR)

        print(':: Generating transition frames... ', end='', flush=True)
        utils.show_notification('Generating transition frames',
                                'This may take a few seconds.')

        jobs = [(paths.CACHE_DIR, level, self.transition_steps, self.max_sigma)
                for level in range(self.transition_steps + 1)]

        cpu_count = multiprocessing.cpu_count()
        pool = multiprocessing.Pool(processes=cpu_count)
        pool.starmap(frame.generate, jobs)

        print('\033[32mDone\033[0m')
        utils.show_notification('Transition frames generated',
                                'Ready for fancy blurring!')
