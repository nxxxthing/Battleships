# tests/test_coordinates.py

from Coordinates import Coordinates


def test_coordinates_initialization():
    coord = Coordinates(3, 4)
    assert coord.x == 3
    assert coord.y == 4
    assert coord.is_active


def test_coordinates_set():
    coord = Coordinates(1, 2)
    coord.set(3, 4)
    assert coord.x == 3
    assert coord.y == 4
    assert coord.is_active


def test_coordinates_unset():
    coord = Coordinates(3, 4)
    coord.unset()
    assert coord.x == -1
    assert coord.y == -1
    assert not coord.is_active()
