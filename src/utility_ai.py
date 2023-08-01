from direction import Direction


class UtilityAI:
    """
    Determines the best action for a character based on the utilities of different actions
    """
    def __init__(self, character):
        self.character = character
        self.attack_range = self.character.attacks[str(self.character.name)][1]
        self.max_utility = 0
        self.charge = 0
        self.basic = 0
        self.move = 0
        self.heal = 0

    def smallest_distance(self):
        """
        Returns the smallest distance to a playable character and the Character object in that location
        """
        distances = []
        players = []
        for player in self.character.world.get_play_chars():
            if not player.is_dead():
                distance = self.character.get_location().get_distance(player.get_location())
                distances.append(distance)
                players.append(player)

        min_distance = min(distances)
        index = distances.index(min_distance)
        closest_player = players[index]
        return min_distance, closest_player

    def direction_worth_it(self, loc):
        """
        Returns True if the square in location loc is a viable option and False if the character shouldn't
        move to the square.
        """
        if self.character.world.get_square(loc).is_lava_square():
            if self.character.hp > 5:
                return True
            else:
                return False
        elif self.character.world.get_square(loc).is_empty():
            return True

    def distances(self, locations, player_loc):
        """
        Creates lists that store the absolute distance to the player and the sum of
        changes in the x and y directions in relation to the player.
        """
        distances = []
        dxdy = []
        for loc in locations:
            if self.direction_worth_it(loc):
                dx = player_loc.delta_x(loc)
                dy = player_loc.delta_y(loc)
                dist = player_loc.get_distance(loc)
                distances.append(dist)
                dxdy.append(dx + dy)
            else:
                distances.append(100)
                dxdy.append(100)
        return distances, dxdy

    def direction_nearest(self):
        """
        Returns the direction in which the character should move
        """
        loc_north = self.character.get_location().get_neighbor(Direction.NORTH)
        loc_east = self.character.get_location().get_neighbor(Direction.EAST)
        loc_south = self.character.get_location().get_neighbor(Direction.SOUTH)
        loc_west = self.character.get_location().get_neighbor(Direction.WEST)
        player_loc = self.smallest_distance()[1].get_location()
        locations = [loc_north, loc_east, loc_south, loc_west]

        distances, dxdy = self.distances(locations, player_loc)

        dist_north = distances[0]
        dist_east = distances[1]
        dist_south = distances[2]
        dist_west = distances[3]

        dxdy_north = dxdy[0]
        dxdy_east = dxdy[1]
        dxdy_south = dxdy[2]
        dxdy_west = dxdy[3]

        distances.sort()
        dxdy.sort()

        min_dist = distances[0]
        min_dxdy = dxdy[0]

        if min_dist == dist_north and min_dxdy == dxdy_north:
            return Direction.NORTH
        elif min_dist == dist_east and min_dxdy == dxdy_east:
            return Direction.EAST
        elif min_dist == dist_south and min_dxdy == dxdy_south:
            return Direction.SOUTH
        else:
            return Direction.WEST

    def move_towards_utility(self):
        self.move = 0
        if self.smallest_distance()[0] == self.attack_range + 1:
            self.move = 1
        else:
            self.move = 0.5
        return self.move * 0.5

    def basic_attack_utility(self):
        self.basic = 0
        if self.character.energy >= 1:
            if self.smallest_distance()[0] <= self.attack_range:
                self.basic = 1
        return self.basic * 1

    def charged_attack_utility(self):
        self.charge = 0
        if self.character.energy > 5:
            if self.smallest_distance()[0] <= self.attack_range:
                self.charge = 1
        return self.charge * 2

    def heal_utility(self):
        self.heal = 0
        if self.character.hp < self.character.max_hp - 5:
            self.heal = 1

        return self.heal * 1


    def highest_utility(self):
        self.heal = self.heal_utility()
        self.move = self.move_towards_utility()
        self.basic = self.basic_attack_utility()
        self.charge = self.charged_attack_utility()

        max_utility = max(self.move, self.basic, self.heal, self.charge)

        self.max_utility = max_utility
        return self.max_utility

    def act_on_highest_utility(self):
        max_utility = self.highest_utility()
        if max_utility == self.charge:
            self.action = self.character.charged_attack(self.smallest_distance()[1])
        elif max_utility == self.basic:
            self.action = self.character.basic_attack(self.smallest_distance()[1])
        elif max_utility == self.heal:
            self.action = self.character.heal()
        else:
            self.action = self.character.move(self.direction_nearest())
