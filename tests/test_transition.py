"""
Test cases for the transition thread.

Author: Benedikt Vollmerhaus
License: MIT
"""

import time
from unittest import mock

from blurwal.transition import Transition


def change_to_with_delay(_path: str):
    """
    Mock wallpaper.change_to with sleep to simulate feh doing work.
    """
    time.sleep(1)


@mock.patch('blurwal.wallpaper.change_to')
def test_run_blur(mock_change_to):
    thread = Transition(1, 9)
    thread.start()
    time.sleep(0.1)
    assert mock_change_to.call_count == 8


@mock.patch('blurwal.wallpaper.change_to')
def test_run_unblur(mock_change_to):
    thread = Transition(8, 2)
    thread.start()
    time.sleep(0.1)
    assert mock_change_to.call_count == 6


@mock.patch('blurwal.wallpaper.change_to', side_effect=change_to_with_delay)
def test_stop_cancels_transition(mock_change_to):
    thread = Transition(0, 10)
    thread.start()
    thread.stop()
    assert thread.is_stopped()
    assert mock_change_to.call_count == 1
