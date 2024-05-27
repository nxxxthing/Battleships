# main.py
from Runner import Runner
from Test1 import *

# Usage example:
if __name__ == "__main__":
    runner = Runner(grid_size, n_ships, ships, vertical_limit, horizontal_limit)
    try:
        runner.run()
        print("Found solution:")
        runner.print_grid()
    except ValueError as e:
        print(e)
    except RuntimeError as e:
        print(e)
