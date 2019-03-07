from pytest import approx

from blurwal import utils


def test_map_range_with_positive():
    assert utils.map_range(0.5, (0, 1), (0, 10)) == 5
    assert utils.map_range(2, (0, 10), (0, 1)) == 0.2

    assert utils.map_range(128, (0, 255), (0, 1)) == approx(0.5019607)
    assert utils.map_range(6, (10, 48), (5, 9)) == approx(4.578947)


def test_map_range_with_negative():
    assert utils.map_range(0.5, (0, 1), (0, -10)) == -5
    assert utils.map_range(-2, (0, -10), (0, 1)) == 0.2
    assert utils.map_range(-8, (0, -10), (0, -1)) == -0.8


def test_map_range_with_out_of_range_values():
    assert utils.map_range(6, (0, 1), (0, 10)) == 60
    assert utils.map_range(20.5, (10, 20), (0, 10)) == 10.5

    assert utils.map_range(5.2, (10, 20), (0, 10)) == -4.8
    assert utils.map_range(-4, (0, 1), (1, 2)) == -3


def test_show_notification(mocker):
    mock_run = mocker.patch('subprocess.run')
    utils.show_notification('A Title', 'Hello World')
    mock_run.assert_called_once_with(
        ['notify-send', 'A Title', 'Hello World'])


def test_show_notification_libnotify_is_optional(mocker):
    mocker.patch('subprocess.run', side_effect=FileNotFoundError())
    utils.show_notification('A Title', 'Hello World')
