from src.direction import Direction
from coordinates import Coordinates
from utility_ai import UtilityAI


class Character():

    def __init__(self, name, is_enemy):
        self.name = name # Määrittää hahmon tehtävän (normal, shoot, tank)
        self.world = None
        self.location = None
        self.dead = False   # are they dead
        self.is_enemy = is_enemy # onko vihollisjoukko
        self.attacks = {}
        self.facing = None
        self.damage = None

        self.hp = 10
        self.energy = 10 # tää laskee vedessä ja erikoishyökkäyksen jälkeen
        self.max_hp = 10

        self.ai = None


    def get_world(self):
        return self.world

    def get_location(self):
        return self.location

    def get_location_square(self):
        return self.get_world().get_square(self.get_location())

    def get_facing(self):
        return self.facing

    def is_dead(self):
        if self.hp <= 0:
            self.dead = True
        return self.dead

    def is_stuck(self):
        world = self.get_world()
        if world is None:
            return True
        for value in Direction.get_values():
            if not world.get_square(self.get_location().get_neighbor(value)).is_tree_square():
                return False
        return True

    def set_world(self, world,  location,  facing):
        target_square = world.get_square(location)
        if not target_square.is_empty() or self.get_world() is not None:
            return False
        else:
            self.world = world
            self.location = location
            self.facing = facing
            return True

    def spin(self, new_facing):
        if not self.is_dead():
            self.facing = new_facing

    def move(self, direction):
        if self.is_dead():
            return False

        target = self.get_location().get_neighbor(direction)
        current_square = self.get_location_square()
        target_square = self.get_world().get_square(target)
        self.spin(direction)
        if target_square.is_empty():
            current_square.remove_play_char()
            self.location = target
            target_square.set_play_char(self)

            if target_square.is_water_square():
                self.energy -= 3

            if target_square.is_lava_square():
                self.hp -= 2
            self.raise_energy()
            return True
        else:
            return False

    def move_forward(self):
        return self.move(self.get_facing())

    def basic_attack(self, victim):
        for key, value in self.attacks.items():
            if "charge" not in key:
                if self.get_location().get_distance(victim.get_location()) <= self.attacks[key][1]:
                    victim.hp = victim.hp - self.attacks[key][0]
                    self.raise_energy()
                    return True
                else:
                    return False

    def charged_attack(self, victim):
        for key, value in self.attacks.items():
            if "charge" in key:
                if self.get_location().get_distance(victim.get_location()) <= self.attacks[key][1]:
                    if self.energy > 5:
                        self.energy -= 5
                        victim.hp = victim.hp - self.attacks[key][0]
                        return True
                else:
                    return False

    def raise_energy(self):
        if self.energy < 10:
            self.energy += 1

    def heal(self):
        if self.hp < self.max_hp:
            self.hp += 1
            self.raise_energy()

    def add_ai(self):
        if self.is_enemy:
            self.ai = UtilityAI(self)
