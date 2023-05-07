from src.direction import Direction

class Character():

    def __init__(self, name, is_enemy):
        self.name = name
        self.world = None    # fixed value
        self.location = None   # most-recent holder
        self.dead = False   # are they dead
        self.is_enemy = is_enemy # onko vihollisjoukko
        self.facing = None
        self.damage = None
        self.hp = 8
        self.max_hp = 10

    def get_world(self):
        return self.world

    def get_location(self):
        return self.location

    def get_location_square(self):
        return self.get_world().get_square(self.get_location())

    def get_facing(self):
        return self.facing

    def is_dead(self):
        if self.hp == 0:
            self.dead = True
        return self.dead

    def is_stuck(self):
        world = self.get_world()
        if world is None:
            return True
        # Tätä pitää muistaa muokata, että se ottaa huomioon muutkin kun puut eli hahmot jne.
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
            return True
        else:
            return False

    def move_forward(self):
        return self.move(self.get_facing())

    #Hyökkäys, johon tarvitaan target ja attack type

    def attack(self, victim):
        victim.hp = victim.hp - 1

    def heal(self):
        if self.hp < self.max_hp:
            self.hp += 1
