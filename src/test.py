import unittest
from player import Player
from gameworld import GameWorld
from coordinates import Coordinates
from direction import Direction
from square import Square


class TestGameWorld(unittest.TestCase):
    def test_init(self):
        world = GameWorld(10,10)

        self.assertEqual(world.get_width(), 10)
        self.assertEqual(world.get_height(), 10)
        self.assertEqual(world.get_play_chars(), [])


class TestPlayer(unittest.TestCase):
    def test_move(self):
        world = GameWorld(10,10)
        coordinates = Coordinates(0,0)
        player = Player("a")
        world.add_play_char(player, coordinates, Direction.WEST)
        player.move(Direction.EAST)

        self.assertEqual(player.get_location().get_x(), 1)
        self.assertEqual(player.get_location().get_y(), 0)
        self.assertEqual(player.get_facing(), Direction.EAST)


class TestSquare(unittest.TestCase):
    def test_set_player(self):
        square = Square()
        player = Player("a")
        square.set_play_char(player)
        self.assertEqual(square.get_play_char(), player)

    def set_player_when_not_empty(self):
        square = Square()
        square.set_lava()

        self.assertFalse(square.set_play_char(Player("aa")))



