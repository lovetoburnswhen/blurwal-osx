"""
Test cases for the frame module.

Author: Benedikt Vollmerhaus
License: MIT
"""

from pathlib import Path

from blurwal import frame


def test_generate_runs_convert(mocker):
    mocker.patch('blurwal.wallpaper.get_original', return_value='image.png')
    mock_run = mocker.patch('subprocess.run')

    output_dir = Path('~/.cache/blurwal')
    expected_output_file = str(output_dir / 'frame-4.jpg')

    frame.generate(output_dir, 4, 10, 12)
    mock_run.assert_called_once_with(
        ['convert', 'image.png', '-blur', '0x4.8', expected_output_file])


def test_is_outdated_false_when_equal(mocker, shared_datadir):
    mocker.patch('blurwal.frame.generate')
    mocker.patch('blurwal.paths.CACHE_DIR', shared_datadir / 'cache_dir')
    mocker.patch('blurwal.paths.TEMP_DIR', shared_datadir / 'temp_dir')
    assert not frame.is_outdated(5, 0, 0)


def test_is_outdated_true_when_different(mocker, shared_datadir):
    mocker.patch('blurwal.frame.generate')
    mocker.patch('blurwal.paths.CACHE_DIR', shared_datadir / 'cache_dir')
    mocker.patch('blurwal.paths.TEMP_DIR', shared_datadir / 'temp_dir_differs')
    assert frame.is_outdated(5, 0, 0)
