from direction import Direction

class Player():

    def __init__(self, name):
        self.set_name(name)
        self.world = None    # fixed value
        self.location = None   # most-recent holder
        self.dead = False   # are they dead
        self.facing = None
        self.hp = 10

    def set_name(self, name):
        self.name = "Mr. Carson"

    def get_world(self):
        return self.world

    def get_location(self):
        return self.location

    def get_location_square(self):
        return self.get_world().get_square(self.get_location())

    def get_facing(self):
        return self.facing

    def kill(self):
        self.dead = True

    def is_dead(self):
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
            return True
        else:
            return False

    def move_forward(self):
        return self.move(self.get_facing())
