"""
Module containing unit tests for the Runner class in the runner.py file.
"""
from io import StringIO
import sys

import pytest

from runner import Runner
from ship import Ship
from test_data import GRID_SIZE, N_SHIPS, ships, vertical_limit, horizontal_limit


def test_runner_no_solution():
    """
    Test if Runner raises RuntimeError and ValueError when there's no solution.

    """
    runner = Runner(grid_size=2, n_ships=2, ships=[Ship(1), Ship(1)], vertical_limit=[[], []], horizontal_limit=[[],[]])

    with pytest.raises(RuntimeError):
        runner.result()

    with pytest.raises(ValueError):
        runner.run()


def test_runner_get_orientation():
    """
    Test if Runner correctly returns the orientation based on input.

    """
    assert Runner.get_orientation('horizontal') == [1, 0]


def test_runner_run():
    """
    Test if Runner correctly indicates that not all ships are placed.

    """
    runner = Runner(grid_size=GRID_SIZE, n_ships=N_SHIPS, ships=ships, vertical_limit=vertical_limit,
                    horizontal_limit=horizontal_limit)
    assert runner.all_ships_placed() is False


def test_runner_run_2():
    """
    Test if Runner correctly indicates that all ships are placed after running.

    """
    runner = Runner(grid_size=GRID_SIZE, n_ships=N_SHIPS, ships=ships, vertical_limit=vertical_limit,
                    horizontal_limit=horizontal_limit)
    runner.run()
    assert runner.all_ships_placed()


def test_place_required_horizontal():
    """
    Test if place_required_horizontal method behaves as expected.

    """
    runner = Runner(grid_size=GRID_SIZE, n_ships=N_SHIPS, ships=ships, vertical_limit=vertical_limit,
                    horizontal_limit=horizontal_limit)
    assert runner.place_required_horizontal(2)


def test_print_grid():
    """
    Test if print_grid method outputs the grid correctly.

    """
    runner = Runner(grid_size=GRID_SIZE, n_ships=N_SHIPS, ships=ships, vertical_limit=vertical_limit,
                    horizontal_limit=horizontal_limit)
    runner.grid = [[1, 0, 0], [0, 2, 0], [0, 0, 3]]
    runner.grid_size = 3

    sys.stdout = StringIO()

    runner.print_grid()

    printed_output = sys.stdout.getvalue()

    sys.stdout = sys.__stdout__

    expected_grid = "|1| | |\n| |2| |\n| | |3|\n"

    assert printed_output == expected_grid


def test_ship_placement():
    """
    Test if ship placement method places the ship correctly.

    """
    runner = Runner(grid_size=GRID_SIZE, n_ships=N_SHIPS, ships=ships, vertical_limit=vertical_limit,
                    horizontal_limit=horizontal_limit)
    assert runner.place_ship(0, 0, 0, 'horizontal')
    assert runner.grid[0][0] == 1


def test_runner_run_fails():
    """
    Test if Runner raises ValueError when it fails to find a solution.

    """
    fail_ships = [
        Ship(3),
        Ship(3),
        Ship(3),
        Ship(3),
        Ship(3),
        Ship(3),
    ]
    runner = Runner(grid_size=GRID_SIZE, n_ships=N_SHIPS, ships=fail_ships, vertical_limit=vertical_limit,
                    horizontal_limit=horizontal_limit)
    with pytest.raises(ValueError):
        runner.run()
