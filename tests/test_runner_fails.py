# tests/test_runner.py
import pytest

from Runner import Runner
from TestValidation import *


def test_runner_run():
    runner = Runner(grid_size=grid_size, n_ships=n_ships, ships=ships, vertical_limit=vertical_limit,
                    horizontal_limit=horizontal_limit)
    with pytest.raises(ValueError):
        runner.run()
