from pathlib import Path

import pytest

from blurwal import paths, wallpaper


def test_change_to_runs_feh(mocker):
    mock_run = mocker.patch('subprocess.run')
    wallpaper.change_to('~/images/wallpaper.png')
    mock_run.assert_called_once_with(
        ['feh', '--bg-fill', '~/images/wallpaper.png'])


def test_is_transition(mocker):
    mocker.patch('blurwal.wallpaper.get_current',
                 return_value=str(paths.CACHE_DIR / 'frame-4.png'))
    assert wallpaper.is_transition()


def test_is_transition_false_when_name_not_frame(mocker):
    mocker.patch('blurwal.wallpaper.get_current',
                 return_value=str(paths.CACHE_DIR / 'wallpaper.png'))
    assert not wallpaper.is_transition()


def test_is_transition_false_when_not_in_cache_dir(mocker):
    mocker.patch('blurwal.wallpaper.get_current',
                 return_value=str(Path.home() / 'frame-4.png'))
    assert not wallpaper.is_transition()


def test_get_current(mocker, datadir):
    mocker.patch('blurwal.paths.FEHBG_FILE', datadir / '.fehbg')
    assert wallpaper.get_current() == '/home/user/images/wallpaper.png'


def test_get_current_with_all_quoted_fehbg(mocker, datadir):
    mocker.patch('blurwal.paths.FEHBG_FILE', datadir / '.fehbg_all_quoted')
    assert wallpaper.get_current() == '/home/user/images/wallpaper.png'


def test_get_current_exits_when_fehbg_invalid(mocker, datadir):
    mocker.patch('blurwal.paths.FEHBG_FILE', datadir / '.fehbg_invalid')
    with pytest.raises(SystemExit):
        wallpaper.get_current()


def test_get_current_exits_when_fehbg_missing(mocker, datadir):
    mocker.patch('blurwal.paths.FEHBG_FILE', datadir / 'missing/.fehbg')
    with pytest.raises(SystemExit):
        wallpaper.get_current()


def test_get_original(mocker, datadir):
    mocker.patch('blurwal.paths.ORIGINAL_PATH', datadir / 'original-path')
    assert wallpaper.get_original() == '/home/user/images/wallpaper.png'


def test_set_original(mocker, datadir):
    original_path = datadir / 'original-path'
    mocker.patch('blurwal.paths.ORIGINAL_PATH', original_path)

    wallpaper.set_original('/home/user/images/new_wallpaper.png')
    assert original_path.read_text() == '/home/user/images/new_wallpaper.png'


def test_restore_original(mocker):
    mocker.patch('blurwal.wallpaper.get_original',
                 return_value='~/images/wallpaper.png')
    mock_change_to = mocker.patch('blurwal.wallpaper.change_to')
    wallpaper.restore_original()
    mock_change_to.assert_called_once_with('~/images/wallpaper.png')


def test_restore_original_exits_when_missing(mocker):
    mocker.patch('blurwal.wallpaper.get_original',
                 side_effect=FileNotFoundError())
    with pytest.raises(SystemExit):
        wallpaper.restore_original()
