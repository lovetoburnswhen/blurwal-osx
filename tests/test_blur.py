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
    args = Namespace(min=2, steps=10, blur=0, ignore=[])
    blur = Blur(args)

    blur_thread = Transition(0, 0)
    unblur_thread = Transition(0, 0)

    mock_transition = mocker.patch('blurwal.blur.Transition')
    blur.init_transition(2, blur_thread, unblur_thread)
    mock_transition.assert_called_once_with(0, 10)


def test_init_transition_unblurs_when_under_threshold(mocker):
    args = Namespace(min=2, steps=10, blur=0, ignore=[])
    blur = Blur(args)

    blur_thread = Transition(0, 0)
    blur_thread.current_level = 10  # Blur thread has completed
    unblur_thread = Transition(0, 0)

    mock_transition = mocker.patch('blurwal.blur.Transition')
    blur.init_transition(0, blur_thread, unblur_thread)
    mock_transition.assert_called_once_with(10, 0)


def test_init_transition_does_not_blur_consecutively(mocker):
    mocker.patch('blurwal.wallpaper.change_to')
    args = Namespace(min=2, steps=10, blur=0, ignore=[])
    blur = Blur(args)

    # Blur as previous transition
    blur_thread, unblur_thread = blur.init_transition(
        2, Transition(0, 0), Transition(0, 0))

    mock_transition = mocker.patch('blurwal.blur.Transition')

    # Should not blur again consecutively
    blur.init_transition(2, blur_thread, unblur_thread)
    mock_transition.assert_not_called()


def test_init_transition_does_not_unblur_consecutively(mocker):
    mocker.patch('blurwal.wallpaper.change_to')
    args = Namespace(min=2, steps=10, blur=0, ignore=[])
    blur = Blur(args)

    # Unblur as previous transition
    blur_thread, unblur_thread = blur.init_transition(
        0, Transition(0, 0), Transition(0, 0))

    mock_transition = mocker.patch('blurwal.blur.Transition')

    # Should not unblur again consecutively
    blur.init_transition(0, blur_thread, unblur_thread)
    mock_transition.assert_not_called()


def test_frames_are_outdated(mocker, shared_datadir):
    mocker.patch('blurwal.paths.CACHE_DIR', shared_datadir / 'cache_dir')
    mocker.patch('blurwal.frame.is_outdated', return_value=False)

    args = Namespace(steps=10, blur=0, min=0, ignore=[])
    blur = Blur(args)
    assert not blur.frames_are_outdated()


def test_frames_are_outdated_when_frame_missing(mocker, shared_datadir):
    mocker.patch('blurwal.paths.CACHE_DIR', shared_datadir / 'cache_dir')
    args = Namespace(steps=11, blur=0, min=0, ignore=[])
    blur = Blur(args)
    assert blur.frames_are_outdated()


def test_frames_are_outdated_when_frame_outdated(mocker, shared_datadir):
    mocker.patch('blurwal.paths.CACHE_DIR', shared_datadir / 'cache_dir')
    mocker.patch('blurwal.frame.is_outdated', return_value=True)

    args = Namespace(steps=10, blur=0, min=0, ignore=[])
    blur = Blur(args)
    assert blur.frames_are_outdated()


def test_generate_transition_frames(mocker):
    mocker.patch('blurwal.utils.show_notification')
    mock_starmap = mocker.patch.object(Pool, 'starmap')

    args = Namespace(steps=10, blur=8.5, min=0, ignore=[])
    blur = Blur(args)

    expected_jobs = [(paths.CACHE_DIR, l, 10, 8.5) for l in range(11)]

    blur.generate_transition_frames()
    mock_starmap.assert_called_once_with(frame.generate, expected_jobs)
