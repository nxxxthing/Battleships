# test.py
"""
Testing data
"""
from ship import Ship

GRID_SIZE = 5
N_SHIPS = 6
ships = [
    Ship(1),
    Ship(1),
    Ship(1),
    Ship(2),
    Ship(2),
    Ship(3),
]

vertical_limit = [
    [1],
    [],
    [2, 2],
    [],
    [2, 1]
]

horizontal_limit = [
    [2, 1],
    [],
    [1, 1],
    [],
    [1]
]
