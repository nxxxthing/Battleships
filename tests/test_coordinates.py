"""
Tests for Coordinates class
"""

from coordinates import Coordinates


def test_coordinates_initialization():
    """
    Test coordinates initialization
    """
    coord = Coordinates(3, 4)
    assert coord.x == 3
    assert coord.y == 4
    assert coord.is_active


def test_coordinates_set():
    """
    Test coordinates set
    """
    coord = Coordinates(1, 2)
    coord.set(3, 4)
    assert coord.x == 3
    assert coord.y == 4
    assert coord.is_active


def test_coordinates_unset():
    """
    Test coordinates unset
    """
    coord = Coordinates(3, 4)
    coord.unset()
    assert coord.x == -1
    assert coord.y == -1
    assert not coord.is_active()
