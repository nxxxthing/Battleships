from Coordinates import Coordinates


class Runner:

    def __init__(self, grid_size, n_ships, ships, vertical_limit, horizontal_limit):
        self.grid_size = grid_size
        self.n_ships = n_ships
        self.ships = ships
        self.vertical_limit = vertical_limit
        self.horizontal_limit = horizontal_limit

        self.ships_coordinates = [Coordinates() for _ in range(self.n_ships)]
        self.hasToBePlaced = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.solution_found = False


    def is_outside_of_grid(self, x, y):
        return x < 0 or y < 0 or x >= self.grid_size or y >= self.grid_size

    def cell_is_free_or_outside(self, x, y):
        if self.is_outside_of_grid(x, y):
            return True
        return self.grid[x][y] == 0

    def cell_has_no_neighbours(self, x, y):
        return (self.cell_is_free_or_outside(x - 1, y) and self.cell_is_free_or_outside(x + 1, y) and
                self.cell_is_free_or_outside(x, y - 1) and self.cell_is_free_or_outside(x, y + 1) and
                self.cell_is_free_or_outside(x + 1, y - 1) and self.cell_is_free_or_outside(x + 1, y + 1) and
                self.cell_is_free_or_outside(x - 1, y - 1) and self.cell_is_free_or_outside(x - 1, y + 1))

    def print_grid(self):
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                print('|', end='')
                if self.grid[x][y] >= 1:
                    print(self.grid[x][y], end='')
                else:
                    print(" ", end='')
            print('|')

    def required_outside_or_free(self, x, y):
        return self.is_outside_of_grid(x, y) or self.hasToBePlaced[x][y] == 0

    def can_place_required(self, x, y):
        return (self.required_outside_or_free(x - 1, y - 1) and self.required_outside_or_free(x - 1, y + 1) and
                self.required_outside_or_free(x + 1, y - 1) and self.required_outside_or_free(x + 1, y + 1))

    def ship_can_be_placed(self, x, y, length, x_change, y_change):
        if length <= 0:
            return True
        return (not self.is_outside_of_grid(x, y) and self.cell_has_no_neighbours(x, y) and
                self.grid[x][y] == 0 and self.can_place_required(x, y) and
                self.ship_can_be_placed(x + x_change, y + y_change, length - 1, x_change, y_change))

    def put_ship_in_cell(self, x, y, length, x_change, y_change, ship_index):
        if length <= 0:
            return
        self.grid[x][y] = ship_index + 1
        self.put_ship_in_cell(x + x_change, y + y_change, length - 1, x_change, y_change, ship_index)

    def place_ship(self, x, y, ship_index, x_change, y_change):
        length = self.ships[ship_index].length
        if self.ship_can_be_placed(x, y, length, x_change, y_change):
            self.put_ship_in_cell(x, y, length, x_change, y_change, ship_index)
            self.ships_coordinates[ship_index] = Coordinates(x, y)
            return True
        return False

    def remove_ship(self, x, y):
        if self.is_outside_of_grid(x, y) or self.grid[x][y] == 0:
            return
        self.grid[x][y] = 0
        self.remove_ship(x + 1, y)
        self.remove_ship(x - 1, y)
        self.remove_ship(x, y + 1)
        self.remove_ship(x, y - 1)

    def check_horizontal(self, x):
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
        if self.all_ships_placed():
            return True

        if self.is_outside_of_grid(x, y):
            if x < self.grid_size <= y:
                if not self.check_horizontal(x):
                    return False
                return self.try_to_place_ships(x + 1, 0)
            return False

        if self.grid[x][y] == 0:
            checked_sizes = [0] * self.grid_size
            for ship_number in range(self.n_ships):
                if self.ships_coordinates[ship_number].is_active() or checked_sizes[self.ships[ship_number].length] == 1:
                    continue
                checked_sizes[self.ships[ship_number].length] = 1
                if self.place_ship(x, y, ship_number, 1, 0):
                    if self.try_to_place_ships(x, y + 1):
                        return True
                    self.ships_coordinates[ship_number] = Coordinates()
                    self.remove_ship(x, y)
                if self.place_ship(x, y, ship_number, 0, 1):
                    if self.try_to_place_ships(x, y + 1):
                        return True
                    self.ships_coordinates[ship_number] = Coordinates()
                    self.remove_ship(x, y)

        if self.hasToBePlaced[x][y] == 1:
            return False

        if x == self.grid_size - 1 and not self.check_vertical(y):
            return False

        return self.try_to_place_ships(x, y + 1)

    def place_required_vertical(self, y):
        limit_index = 0
        for x in range(self.vertical_limit[y][limit_index], self.grid_size, self.vertical_limit[y][limit_index] + 1):
            if self.can_place_required(x, y):
                self.hasToBePlaced[x][y] = 1
            else:
                return False
        return True

    def place_required_horizontal(self, x):
        limit_index = 0
        for y in range(self.horizontal_limit[x][limit_index], self.grid_size, self.horizontal_limit[x][limit_index] + 1):
            if self.can_place_required(x, y):
                self.hasToBePlaced[x][y] = 1
            else:
                return False
        return True

    def validate_limits(self):
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
        if not self.validate_limits():
            raise ValueError("Limits are wrong, no solution can be found")
        self.solution_found = self.try_to_place_ships(0, 0)
        if not self.solution_found:
            raise ValueError("No solution found")

    def result(self):
        if not self.solution_found:
            raise RuntimeError("Run method was not called or no solution was found")
        return self.grid
