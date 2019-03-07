import logging

import pytest

import blurwal.__main__
from blurwal import paths


def test_parse_args_exits_when_steps_below_2():
    with pytest.raises(SystemExit):
        blurwal.__main__.parse_args(['-s', '1'])


def test_parse_args_verbose_sets_log_level():
    blurwal.__main__.parse_args(['--verbose'])
    assert logging.getLogger().getEffectiveLevel() == logging.INFO


def test_parse_args_debug_sets_log_level():
    blurwal.__main__.parse_args(['--debug'])
    assert logging.getLogger().getEffectiveLevel() == logging.DEBUG


def test_prepare_environment_creates_directories(mocker, tmp_path):
    mocker.patch('blurwal.wallpaper.restore_original')

    # Should create blurwal/ subdirectory in ~/.cache
    mocker.patch('blurwal.paths.CACHE_DIR', tmp_path / '.cache/blurwal')
    # Should create blurwal/ subdirectory in temp directory
    mocker.patch('blurwal.paths.TEMP_DIR', tmp_path / 'blurwal')

    blurwal.__main__.prepare_environment()

    assert paths.CACHE_DIR.is_dir()
    assert paths.TEMP_DIR.is_dir()


def test_main_restores_original_when_transition(mocker):
    mocker.patch('blurwal.__main__.Blur')
    mocker.patch('blurwal.__main__.parse_args')
    mocker.patch('blurwal.__main__.prepare_environment')

    mocker.patch('blurwal.wallpaper.is_transition', return_value=True)
    mock_restore_original = mocker.patch('blurwal.wallpaper.restore_original')
    blurwal.__main__.main()
    mock_restore_original.assert_called_once()


def test_main_sets_original_when_not_transition(mocker):
    mocker.patch('blurwal.__main__.Blur')
    mocker.patch('blurwal.__main__.parse_args')
    mocker.patch('blurwal.__main__.prepare_environment')

    mocker.patch('blurwal.wallpaper.is_transition', return_value=False)
    mocker.patch('blurwal.wallpaper.get_current', return_value='image.png')
    mock_set_original = mocker.patch('blurwal.wallpaper.set_original')
    blurwal.__main__.main()
    mock_set_original.assert_called_once_with('image.png')
