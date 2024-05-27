class Coordinates:
    def __init__(self, x=-1, y=-1):
        self.x = x
        self.y = y
        self.__is_active = x != -1 and y != -1

    def is_active(self):
        return self.__is_active

    def set(self, x_coord, y_coord):
        self.x = x_coord
        self.y = y_coord
        self.__is_active = True

    def unset(self):
        self.x = -1
        self.y = -1
        self.__is_active = False
