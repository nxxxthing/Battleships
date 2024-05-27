"""
Module representing coordinates in the game.
"""


class Coordinates:
    """
    Represents coordinates in the game grid.

    Attributes:
        x (int): The x-coordinate.
        y (int): The y-coordinate.
        __is_active (bool): Flag indicating if the coordinates are active.
    """
    def __init__(self, x=-1, y=-1):
        self.x = x
        self.y = y
        self.__is_active = x != -1 and y != -1

    def is_active(self):
        """
        Check if the coordinates are active.

        Returns:
            bool: True if the coordinates are active, False otherwise.
        """
        return self.__is_active

    def set(self, x_coord, y_coord):
        """
        Set new coordinates for the object.

        Parameters:
            x_coord (int): The new x-coordinate.
            y_coord (int): The new y-coordinate.
        """
        self.x = x_coord
        self.y = y_coord
        self.__is_active = True

    def unset(self):
        """Unset the coordinates, setting them to (-1, -1)."""
        self.x = -1
        self.y = -1
        self.__is_active = False
