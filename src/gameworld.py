from square import Square
import random

class GameWorld():

    def __init__ (self, width, height):
        self.squares = [None] * width
        for x in range(self.get_width()):      # stepper
            self.squares[x] = [None] * height
            for y in range(self.get_height()):    # stepper
                self.squares[x][y] = Square()    # fixed value
        self.play_chars = []                        # container
        self.enemies = []
        self.player_turn = True
        self.game_won = False

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

    def add_ai(self):
        for enemy in self.enemies:
            enemy.add_ai()

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

    def choose_enemy(self):
        highest_utility = 0.25
        utilities = []
        chosen_enemy = None
        for enemy in self.enemies:
            if not enemy.is_dead():
                utility = enemy.ai.highest_utility()
                utilities.append(utility)
                if utility > highest_utility:
                    highest_utility = utility
                    chosen_enemy = enemy

        if max(utilities) == 0.25:
            index = random.randint(1, len(self.enemies))
            print(index - 1)
            chosen_enemy = self.enemies[index - 1]
        print(str(chosen_enemy.name), str(highest_utility))
        return chosen_enemy

    def enemy_turn(self):
        if not self.player_turn:
            enemy = self.choose_enemy()
            enemy.ai.act_on_highest_utility()
            self.player_turn = True

    def game_over(self):
        enemies_alive = 0
        chars_alive = 0
        for enemy in self.get_enemies():
            if not enemy.is_dead():
                enemies_alive += 1
        for char in self.get_play_chars():
            if not char.is_dead():
                chars_alive += 1
        if chars_alive == 0:
            return -1
        if enemies_alive == 0:
            return 1
        return 0