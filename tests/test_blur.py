"""
Test cases for the main event listener.

Author: Benedikt Vollmerhaus
License: MIT
"""

from argparse import Namespace
from multiprocessing.pool import Pool

from blurwal import frame, paths
from blurwal.blur import Blur
from blurwal.transition import Transition


def test_init_transition_blurs_when_over_threshold(mocker):
    mock_change_to = mocker.patch('blurwal.wallpaper.change_to')
    args = Namespace(steps=10, max=0, threshold=2, ignore=[])
    blur = Blur(args)

    blur.init_transition(2, Transition(0, 0), Transition(0, 0))
    assert mock_change_to.call_count == 10


def test_init_transition_unblurs_when_under_threshold(mocker):
    mocker.patch('blurwal.wallpaper.change_to')
    args = Namespace(steps=10, max=0, threshold=2, ignore=[])
    blur = Blur(args)

    blur_thread, unblur_thread = blur.init_transition(
        2, Transition(0, 0), Transition(0, 0))

    mock_change_to = mocker.patch('blurwal.wallpaper.change_to')

    blur.init_transition(0, blur_thread, unblur_thread)
    assert mock_change_to.call_count == 10


def test_init_transition_does_not_blur_consecutively(mocker):
    mocker.patch('blurwal.wallpaper.change_to')
    args = Namespace(steps=10, max=0, threshold=2, ignore=[])
    blur = Blur(args)

    # Blur as previous transition
    blur_thread, unblur_thread = blur.init_transition(
        2, Transition(0, 0), Transition(0, 0))

    mock_change_to = mocker.patch('blurwal.wallpaper.change_to')

    # Should not blur again consecutively
    blur.init_transition(2, blur_thread, unblur_thread)
    assert mock_change_to.call_count == 0


def test_init_transition_does_not_unblur_consecutively(mocker):
    mocker.patch('blurwal.wallpaper.change_to')
    args = Namespace(steps=10, max=0, threshold=2, ignore=[])
    blur = Blur(args)

    # Unblur as previous transition
    blur_thread, unblur_thread = blur.init_transition(
        0, Transition(0, 0), Transition(0, 0))

    mock_change_to = mocker.patch('blurwal.wallpaper.change_to')

    # Should not unblur again consecutively
    blur.init_transition(0, blur_thread, unblur_thread)
    assert mock_change_to.call_count == 0


def test_frames_are_outdated(mocker, shared_datadir):
    mocker.patch('blurwal.paths.CACHE_DIR', shared_datadir / 'cache_dir')
    mocker.patch('blurwal.frame.is_outdated', return_value=False)

    args = Namespace(steps=10, max=0, threshold=0, ignore=[])
    blur = Blur(args)
    assert not blur.frames_are_outdated()


def test_frames_are_outdated_when_frame_missing(mocker, shared_datadir):
    mocker.patch('blurwal.paths.CACHE_DIR', shared_datadir / 'cache_dir')
    args = Namespace(steps=11, max=0, threshold=0, ignore=[])
    blur = Blur(args)
    assert blur.frames_are_outdated()


def test_frames_are_outdated_when_frame_outdated(mocker, shared_datadir):
    mocker.patch('blurwal.paths.CACHE_DIR', shared_datadir / 'cache_dir')
    mocker.patch('blurwal.frame.is_outdated', return_value=True)

    args = Namespace(steps=10, max=0, threshold=0, ignore=[])
    blur = Blur(args)
    assert blur.frames_are_outdated()


def test_generate_transition_frames(mocker):
    mock_starmap = mocker.patch.object(Pool, 'starmap')
    mocker.patch('blurwal.utils.show_notification')

    args = Namespace(steps=10, max=8.5, threshold=0, ignore=[])
    blur = Blur(args)

    expected_jobs = [(paths.CACHE_DIR, l, 10, 8.5) for l in range(11)]

    blur.generate_transition_frames()
    mock_starmap.assert_called_once_with(frame.generate, expected_jobs)
