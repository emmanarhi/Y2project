from square import Square

class GameWorld():

    def __init__ (self, width, height):
        self.squares = [None] * width
        for x in range(self.get_width()):      # stepper
            self.squares[x] = [None] * height
            for y in range(self.get_height()):    # stepper
                self.squares[x][y] = Square()    # fixed value
        self.play_chars = []                        # container
        self.enemies = []
        self.turn = 0

    def get_width(self):
        return len(self.squares)

    def get_height(self):
        return len(self.squares[0])

    def add_play_char(self, play_char, location, facing):

        if play_char.set_world(self, location, facing):
            self.play_chars.append(play_char)
            self.get_square(location).set_play_char(play_char)
            return True
        else:
            return False

    def add_enemy(self, enemy, location, facing):
        if enemy.set_world(self, location, facing):
            self.enemies.append(enemy)
            self.get_square(location).set_play_char(enemy)
            return True
        else:
            return False

    def add_tree(self, location):
        return self.get_square(location).set_tree()

    def add_water(self, location):
        return self.get_square(location).set_water()

    def add_lava(self, location):
        return self.get_square(location).set_lava()

    def get_square(self, coordinates):

        if self.contains(coordinates):
            return self.squares[coordinates.get_x()][coordinates.get_y()]
        else:
            return Square(True)

    def contains(self, coordinates):
        x_coordinate = coordinates.get_x()
        y_coordinate = coordinates.get_y()
        return 0 <= x_coordinate < self.get_width() and 0 <= y_coordinate < self.get_height()

    def get_play_chars(self):
        """
        Returns an array containing all the characters currently located in this world: list
        """
        return self.play_chars[:]

    def get_enemies(self):
        return self.enemies[:]