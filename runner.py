"""
runner.py - Module for ship placement runner.

This module defines the Runner class, which is responsible for placing ships on a grid
according to specified constraints and configurations.
It implements various algorithms to explore different ship placement possibilities and find a valid solution.

app:
    Runner: Represents a runner for placing ships on a grid.

Constants:
    None

Functions:
    None

Usage:
    To use the Runner class, instantiate it with the required parameters and call the run method to find a solution.

Example:
    from runner import Runner

    grid_size = 10
    n_ships = 5
    ships = [...]  # List of Ship objects
    vertical_limit = [...]  # List of lists specifying vertical constraints
    horizontal_limit = [...]  # List of lists specifying horizontal constraints

    runner = Runner(grid_size, n_ships, ships, vertical_limit, horizontal_limit)
    runner.run()

"""
from coordinates import Coordinates


class Runner:
    """
    Represents a runner for placing ships on a grid.

    This class provides methods for placing ships on a grid based on specified constraints and configurations.
    It implements various algorithms to efficiently explore different ship placement
    possibilities and find a valid solution.

    Attributes:
        grid_size (int): The size of the grid.
        n_ships (int): The number of ships to be placed.
        ships (list): A list of Ship objects representing the ships to be placed.
        vertical_limit (list): A list of lists specifying vertical constraints for ship placement.
        horizontal_limit (list): A list of lists specifying horizontal constraints for ship placement.
        ships_coordinates (list): A list of Coordinates objects representing the coordinates of placed ships.
        hasToBePlaced (list): A grid representing cells that must be filled with ships.
        grid (list): A 2D grid representing the game board.
    """

    def __init__(self, grid_size, n_ships, ships, vertical_limit, horizontal_limit):
        self.grid_size = grid_size
        self.n_ships = n_ships
        self.ships = ships
        self.vertical_limit = vertical_limit
        self.horizontal_limit = horizontal_limit

        self.ships_coordinates = [Coordinates() for _ in range(self.n_ships)]
        self.has_to_be_placed = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.solution_found = False

    def is_outside_of_grid(self, x, y):
        """
        Check if the specified coordinates are outside of the grid boundaries.

        This method checks if the specified coordinates (x, y) are outside of the grid boundaries.

        Parameters:
            x (int): The row index.
            y (int): The column index.

        Returns:
            bool: True if the coordinates are outside of the grid boundaries, False otherwise.
        """
        return x < 0 or y < 0 or x >= self.grid_size or y >= self.grid_size

    def cell_is_free_or_outside(self, x, y):
        """
        Check if the cell at the specified coordinates is either outside of the grid or free.

        This method checks if the cell at the specified coordinates (x, y) is either outside of the grid boundaries
        or free (not occupied by any ship).

        Parameters:
            x (int): The row index.
            y (int): The column index.

        Returns:
            bool: True if the cell is either outside of the grid or free, False otherwise.
        """
        if self.is_outside_of_grid(x, y):
            return True
        return self.grid[x][y] == 0

    def cell_has_no_neighbours(self, x, y):
        """
        Check if the cell at the specified coordinates has no neighboring ships.

        This method checks if the cell at the specified coordinates (x, y) has no neighboring ships by examining the
        adjacent cells (top, bottom, left, right, top-left, top-right, bottom-left, and bottom-right).

        Parameters:
            x (int): The row index.
            y (int): The column index.

        Returns:
            bool: True if the cell has no neighboring ships, False otherwise.
        """
        return (self.cell_is_free_or_outside(x - 1, y) and self.cell_is_free_or_outside(x + 1, y) and
                self.cell_is_free_or_outside(x, y - 1) and self.cell_is_free_or_outside(x, y + 1) and
                self.cell_is_free_or_outside(x + 1, y - 1) and self.cell_is_free_or_outside(x + 1, y + 1) and
                self.cell_is_free_or_outside(x - 1, y - 1) and self.cell_is_free_or_outside(x - 1, y + 1))

    def print_grid(self):
        """
        Print the grid to the console with ship indices or empty cells.

        This method prints the current state of the grid to the console, displaying ship indices for cells containing
        ships and empty cells for cells without ships.
        """
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                print('|', end='')
                if self.grid[x][y] >= 1:
                    print(self.grid[x][y], end='')
                else:
                    print(" ", end='')
            print('|')

    def required_outside_or_free(self, x, y):
        """
        Check if the specified coordinates are outside of the grid or
        if the cell is free according to placement conditions.

        This method checks if the specified coordinates (x, y) are outside of
        the grid boundaries or if the cell is free
        based on the placement conditions, which include being outside of
        the grid or having to be placed according to specific limits.

        Parameters:
            x (int): The row index.
            y (int): The column index.

        Returns:
            bool: True if the coordinates are outside of the grid or if the cell is free, False otherwise.
        """
        return self.is_outside_of_grid(x, y) or self.has_to_be_placed[x][y] == 0

    def can_place_required(self, x, y):
        """
        Check if a ship can be placed at the specified coordinates based on the required placement conditions.

        This method checks if a ship can be placed at the specified coordinates (x, y) based on the required placement
        conditions, which include being outside of the grid or having to be placed according to specific limits.

        Parameters:
            x (int): The row index.
            y (int): The column index.

        Returns:
            bool: True if the ship can be placed at the specified coordinates, False otherwise.
        """
        return (self.required_outside_or_free(x - 1, y - 1) and self.required_outside_or_free(x - 1, y + 1) and
                self.required_outside_or_free(x + 1, y - 1) and self.required_outside_or_free(x + 1, y + 1))

    def ship_can_be_placed(self, x, y, length, orientation):
        """
        Check if a ship can be placed on the grid starting from the given coordinates and extending
        in a specified direction.

        This method recursively checks if a ship of the given length can be placed on the grid starting
        from the specified coordinates (x, y) and extending in the direction specified by the changes
        in the x and y directions (x_change, y_change).

        Parameters:
            x (int): The starting row index.
            y (int): The starting column index.
            length (int): The length of the ship.
            orientation (str): The orientation of the ship ('horizontal' or 'vertical').

        Returns:
            bool: True if the ship can be placed, False otherwise.
        """

        [x_change, y_change] = self.get_orientation(orientation)
        if length <= 0:
            return True
        return (not self.is_outside_of_grid(x, y) and self.cell_has_no_neighbours(x, y) and
                self.grid[x][y] == 0 and self.can_place_required(x, y) and
                self.ship_can_be_placed(x + x_change, y + y_change, length - 1, orientation))

    def put_ship_in_cell(self, coordinates, length, orientation, ship_index):
        """
        Place a ship on the grid starting from the given coordinates and extending in a specified direction.

        This method recursively places a ship on the grid starting from the specified coordinates (x, y)
        and extending in the direction specified by the orientation.
        It fills the grid cells corresponding to the ship with the ship's index plus 1.

        Parameters:
            coordinates (Coordinates): The starting coordinates of the ship.
            length (int): The length of the ship.
            orientation (str): The orientation of the ship ('horizontal' or 'vertical').
            ship_index (int): The index of the ship to be placed.
        """
        x = coordinates.x
        y = coordinates.y
        [x_change, y_change] = self.get_orientation(orientation)
        if length <= 0:
            return
        self.grid[x][y] = ship_index + 1
        self.put_ship_in_cell(Coordinates(x + x_change, y + y_change), length - 1, orientation, ship_index)

    def place_ship(self, x, y, ship_index, orientation):
        """
        Attempt to place a ship on the grid starting from the given coordinates.

        This method tries to place a ship on the grid starting from the specified coordinates (x, y).
        It verifies if the ship can be placed based on its length and the provided orientation.

        Parameters:
            x (int): The starting row index.
            y (int): The starting column index.
            ship_index (int): The index of the ship to be placed.
            orientation (str): The orientation of the ship ('horizontal' or 'vertical').

        Returns:
            bool: True if the ship was successfully placed, False otherwise.
        """

        length = self.ships[ship_index].length
        if self.ship_can_be_placed(x, y, length, orientation):
            self.put_ship_in_cell(Coordinates(x, y), length, orientation, ship_index)
            self.ships_coordinates[ship_index] = Coordinates(x, y)
            return True
        return False

    @staticmethod
    def get_orientation(orientation):
        """
        Determine the changes in the x and y directions based on the orientation.

        This method returns a list containing the changes in the x and y directions based on the specified orientation.
        If the orientation is 'horizontal', the change in the x direction is 1 and the change in the y direction is 0.
        If the orientation is 'vertical', the change in the x direction is 0 and the change in the y direction is 1.

        Parameters:
            orientation (str): The orientation of the ship ('horizontal' or 'vertical').

        Returns:
            list: A list containing two integers representing the changes in the x and y directions, respectively.

        Raises:
            ValueError: If the specified orientation is neither 'horizontal' nor 'vertical'.
        """
        if orientation == 'horizontal':
            return [1, 0]
        if orientation == 'vertical':
            return [0, 1]

        raise ValueError("Invalid orientation. Orientation must be 'horizontal' or 'vertical'.")


    def remove_ship(self, x, y):
        """
        Remove a ship from the grid starting from the given coordinates.

        This method recursively removes a ship from the grid starting from the specified coordinates (x, y).
        It removes the ship by setting the corresponding grid cells to 0.

        Parameters:
            x (int): The starting row index.
            y (int): The starting column index.
        """
        if self.is_outside_of_grid(x, y) or self.grid[x][y] == 0:
            return
        self.grid[x][y] = 0
        self.remove_ship(x + 1, y)
        self.remove_ship(x - 1, y)
        self.remove_ship(x, y + 1)
        self.remove_ship(x, y - 1)

    def check_horizontal(self, x):
        """
        Check if the horizontal ship placement limits are satisfied for the given row index.

        Parameters:
            x (int): The row index to check.

        Returns:
            bool: True if the horizontal placement limits are satisfied, False otherwise.
        """
        limit_index = 0
        gap_size = 0
        for y in range(self.grid_size):
            if limit_index >= len(self.horizontal_limit[x]):
                break
            if self.grid[x][y] > 0:
                if gap_size == 0:
                    continue
                if gap_size != self.horizontal_limit[x][limit_index]:
                    return False
                limit_index += 1
                gap_size = 0
            else:
                gap_size += 1

        return (limit_index >= len(self.horizontal_limit[x]) or
                (limit_index + 1 == len(self.horizontal_limit[x]) and
                 (self.horizontal_limit[x][limit_index] == 0 or gap_size == self.horizontal_limit[x][limit_index])))

    def check_vertical(self, y):
        """
        Check if the vertical ship placement limits are satisfied for the given column index.

        Parameters:
            y (int): The column index to check.

        Returns:
            bool: True if the vertical placement limits are satisfied, False otherwise.
        """
        limit_index = 0
        gap_size = 0
        for x in range(self.grid_size):
            if limit_index >= len(self.vertical_limit[y]):
                break
            if self.grid[x][y] > 0:
                if gap_size == 0:
                    continue
                if gap_size != self.vertical_limit[y][limit_index]:
                    return False
                limit_index += 1
                gap_size = 0
            else:
                gap_size += 1

        return (limit_index >= len(self.vertical_limit[y]) or
                (limit_index + 1 == len(self.vertical_limit[y]) and
                 (self.vertical_limit[y][limit_index] == 0 or gap_size == self.vertical_limit[y][limit_index])))

    def all_ships_placed(self):
        """
        Check if all ships have been successfully placed on the grid.

        Returns:
            bool: True if all ships have been placed, False otherwise.
        """
        for i in range(self.n_ships):
            if not self.ships_coordinates[i].is_active():
                return False
        for x in range(self.grid_size):
            if not self.check_horizontal(x):
                return False
        for y in range(self.grid_size):
            if not self.check_vertical(y):
                return False
        return True

    def try_to_place_ships(self, x, y):
        """
        Attempt to place ships on the grid starting from the given coordinates.

        This method recursively tries to place ships on the grid starting from the specified coordinates (x, y).
        It uses a backtracking algorithm to explore different ship placement possibilities.

        Parameters:
            x (int): The starting row index.
            y (int): The starting column index.

        Returns:
            bool: True if all ships are successfully placed, False otherwise.
        """
        if self.all_ships_placed():
            return True

        if self.is_outside_of_grid(x, y):
            if x < self.grid_size <= y:
                return self.check_horizontal(x) and self.try_to_place_ships(x + 1, 0)
            return False

        if self.grid[x][y] == 0:
            checked_sizes = [0] * self.grid_size
            for ship_number in range(self.n_ships):
                if not self.ships_coordinates[ship_number].is_active() and checked_sizes[
                    self.ships[ship_number].length] != 1:
                    checked_sizes[self.ships[ship_number].length] = 1
                    if (self.place_ship(x, y, ship_number, 'horizontal') and self.try_to_place_ships(x, y + 1)) or \
                            (self.place_ship(x, y, ship_number, 'vertical') and self.try_to_place_ships(x, y + 1)):
                        return True
                    self.ships_coordinates[ship_number] = Coordinates()
                    self.remove_ship(x, y)

        if self.has_to_be_placed[x][y] == 1 or (x == self.grid_size - 1 and not self.check_vertical(y)):
            return False

        return self.try_to_place_ships(x, y + 1)


    def place_required_vertical(self, y):
        """
        Check if placing a ship vertically is required for the given column index.

        Parameters:
            y (int): The column index to check.

        Returns:
            bool: True if placing a ship vertically is required, False otherwise.
        """
        limit_index = 0
        for x in range(self.vertical_limit[y][limit_index], self.grid_size, self.vertical_limit[y][limit_index] + 1):
            if self.can_place_required(x, y):
                self.has_to_be_placed[x][y] = 1
            else:
                return False
        return True

    def place_required_horizontal(self, x):
        """
        Check if placing a ship horizontally is required for the given row index.

        Parameters:
            x (int): The row index to check.

        Returns:
            bool: True if placing a ship horizontally is required, False otherwise.
        """
        limit_index = 0
        for y in range(self.horizontal_limit[x][limit_index], self.grid_size,
                       self.horizontal_limit[x][limit_index] + 1):
            if self.can_place_required(x, y):
                self.has_to_be_placed[x][y] = 1
            else:
                return False
        return True

    def validate_limits(self):
        """
        Validate the limits of ship placement.

        This method checks if the ship placement limits specified by horizontal_limit
        and vertical_limit are valid for the grid size.
        It verifies that the sum of ship lengths and gaps does not exceed
        the size of the grid in both horizontal and vertical directions.

        Returns:
           bool: True if the limits are valid, False otherwise.
        """
        for i in range(self.grid_size):
            sum_horizontal = sum(self.horizontal_limit[i])
            sum_vertical = sum(self.vertical_limit[i])
            horizontal_ships = sum(1 for limit in self.horizontal_limit[i] if limit > 0)
            vertical_ships = sum(1 for limit in self.vertical_limit[i] if limit > 0)
            sum_vertical += max(0, vertical_ships - 1)
            sum_horizontal += max(0, horizontal_ships - 1)
            if sum_vertical > self.grid_size or sum_horizontal > self.grid_size:
                return False
            if sum_vertical == self.grid_size:
                if not self.place_required_vertical(i):
                    return False
            if sum_horizontal == self.grid_size:
                if not self.place_required_horizontal(i):
                    return False
        return True

    def run(self):
        """
        Run the computation to find a solution.

        This method executes the algorithm to find a solution for the problem.
        It modifies the internal state of the Runner object to store the computed result.
        """
        if not self.validate_limits():
            raise ValueError("Limits are wrong, no solution can be found")
        self.solution_found = self.try_to_place_ships(0, 0)
        if not self.solution_found:
            raise ValueError("No solution found")

    def result(self):
        """
        Get the result of the computation.

        Returns:
            list: The computed result.
        """
        if not self.solution_found:
            raise RuntimeError("Run method was not called or no solution was found")
        return self.grid
