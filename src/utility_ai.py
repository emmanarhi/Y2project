from direction import Direction


class UtilityAI:
    def __init__(self, character):
        self.character = character
        self.attack_range = self.character.attacks[str(self.character.name)][1]
        self.max_utility = 0
        self.charge = 0
        self.basic = 0
        self.move = 0
        self.heal = 0

    def smallest_distance(self):
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

    # Funktio määrittää, onko tähän suuntaan kannattavaa liikkua
    def direction_worth_it(self, loc):
        if self.character.world.get_square(loc).is_lava_square():
            if self.character.hp > 5:
                return True
            else:
                return False
        elif self.character.world.get_square(loc).is_empty():
            return True

    def direction_nearest(self):
        loc_north = self.character.get_location().get_neighbor(Direction.NORTH)
        loc_east = self.character.get_location().get_neighbor(Direction.EAST)
        loc_south = self.character.get_location().get_neighbor(Direction.SOUTH)
        loc_west = self.character.get_location().get_neighbor(Direction.WEST)
        player_loc = self.smallest_distance()[1].get_location()

        distances = []

        dist_north = player_loc.get_distance(loc_north)
        if self.direction_worth_it(loc_north):
            distances.append(dist_north)

        dist_east = player_loc.get_distance(loc_east)
        if self.direction_worth_it(loc_east):
            distances.append(dist_east)

        dist_south = player_loc.get_distance(loc_south)
        if self.direction_worth_it(loc_south):
            distances.append(dist_south)

        dist_west = player_loc.get_distance(loc_west)
        if self.direction_worth_it(loc_west):
            distances.append(dist_west)

        distances.sort()
        min_dist = distances[0]

        if min_dist == dist_north:
            return Direction.NORTH
        elif min_dist == dist_east:
            return Direction.EAST
        elif min_dist == dist_south:
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
        elif self.character.hp < self.character.max_hp - 2:
            self.heal = 0.2

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
