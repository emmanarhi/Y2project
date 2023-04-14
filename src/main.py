import sys

from src.gameworld import *
from src.coordinates import *
from player import *
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget
from gui import *

def main():
    test_world = GameWorld(15, 9)
    tree_coordinates = Coordinates(2, 4)
    test_world.add_tree(tree_coordinates)
    water_coordinates = Coordinates(0, 5)
    test_world.add_water(water_coordinates)
    lava_coordinates = Coordinates(0, 0)
    test_world.add_lava(lava_coordinates)

    player = Player("emma")
    player_location = Coordinates(2, 1)
    test_world.add_play_char(player, player_location, Direction.EAST)

    global app  # Use global to prevent crashing on exit
    app = QApplication(sys.argv)
    gui = GUI(test_world, 50)
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
