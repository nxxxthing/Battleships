# tests/test_runner.py
from io import StringIO
import sys
from Runner import Runner
from Test1 import *


def test_runner_run():
    runner = Runner(grid_size=grid_size, n_ships=n_ships, ships=ships, vertical_limit=vertical_limit,
                    horizontal_limit=horizontal_limit)
    assert runner.all_ships_placed() == False
    runner.run()
    assert runner.result() is not None
    assert runner.all_ships_placed()


def test_place_required_horizontal():
    runner = Runner(grid_size=grid_size, n_ships=n_ships, ships=ships, vertical_limit=vertical_limit,
                    horizontal_limit=horizontal_limit)
    assert runner.place_required_horizontal(2)


def test_print_grid():
    runner = Runner(grid_size=grid_size, n_ships=n_ships, ships=ships, vertical_limit=vertical_limit,
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
    runner = Runner(grid_size=grid_size, n_ships=n_ships, ships=ships, vertical_limit=vertical_limit,
                    horizontal_limit=horizontal_limit)
    assert runner.place_ship(0, 0, 0, 1, 0)
    assert runner.grid[0][0] == 1