#!/usr/bin/env python3

"""
Author: Benedikt Vollmerhaus
License: MIT
"""

import argparse
import atexit
import logging
import sys
from typing import List

from blurwal import paths, wallpaper
from blurwal._version import __version__
from blurwal.blur import Blur


def parse_args(arg_list: List) -> argparse.Namespace:
    """
    Parse and return any provided command line arguments.

    :return: A namespace holding the parsed arguments
    """
    parser = argparse.ArgumentParser(
        description='Smoothly blurs the wallpaper when windows are opened.',
        epilog="The transition's speed is based on the chosen number of "
               "steps in combination with how quickly feh can update "
               "the wallpaper on your system. This cannot be changed, as "
               "feh's speed is the limiting upper factor and introducing "
               "a delay between frames to slow things down would lead to "
               "choppy transitions. To vary the transition speed, you "
               "should thus change the number of steps using '-s'.")

    parser.add_argument('-v', '--version',
                        action='version', version=f'%(prog)s {__version__}')

    parser.add_argument('-m', '--min',
                        type=int, metavar='N', default=2,
                        help='the minimum number of windows to blur the '
                             'wallpaper (default: %(default)d)')

    parser.add_argument('-s', '--steps',
                        type=int, metavar='N', default=10,
                        help='the number of steps in a blur transition, '
                             'see below (default: %(default)d, min: 2)')

    parser.add_argument('-b', '--blur',
                        type=int, metavar='N', default=10,
                        help='the blur strength (sigma) to use when '
                             'fully blurred (default: %(default)d)')

    parser.add_argument('-i', '--ignore',
                        nargs='*', metavar='class', default=[],
                        help='a space-separated list of window classes '
                             'to exclude when counting the number of '
                             'open windows')

    parser.add_argument('--verbose',
                        action='store_true',
                        help='print additional information')

    parser.add_argument('--debug',
                        action='store_true',
                        help='print detailed debug output')

    args = parser.parse_args(arg_list)

    if args.steps < 2:
        parser.error('The transition must have at least 2 steps.')

    if args.verbose:
        logging.getLogger().setLevel(logging.INFO)

    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    return args


def prepare_environment() -> None:
    """
    Create the required cache/temp directories if not already existing
    and register an exit handler for restoring the original wallpaper.

    :return: None
    """
    logging.basicConfig(format='%(levelname)s: %(message)s')

    paths.CACHE_DIR.mkdir(parents=True, exist_ok=True)
    paths.TEMP_DIR.mkdir(exist_ok=True)

    atexit.register(wallpaper.restore_original)


def main() -> None:
    """
    Restore the wallpaper if necessary and get ready for blurring!

    :return: None
    """
    prepare_environment()

    if wallpaper.is_transition():
        # If the script terminated unexpectedly and a transition
        # frame got stuck as the wallpaper, restore the original.
        wallpaper.restore_original()
    else:
        wallpaper.set_original(wallpaper.get_current())

    args = parse_args(sys.argv[1:])

    if args.ignore:
        print(f':: Ignoring window classes: {", ".join(args.ignore)}')

    try:
        blur = Blur(args)
        if blur.frames_are_outdated():
            blur.generate_transition_frames()

        blur.listen_for_events()
    except KeyboardInterrupt:
        print('\nBye!')
        sys.exit(0)


if __name__ == '__main__':
    main()
