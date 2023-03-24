import sys
from PyQt6.QtWidgets import QApplication

from gui import GUI

from direction import Direction
from gameworld import *
from coordinates import *
from player import *


def main():
    test_world = GameWorld(15, 9)
    tree_coordinates = Coordinates(2, 4)
    test_world.add_tree(tree_coordinates)
    water_coordinates = Coordinates(0, 5)
    test_world.add_water(water_coordinates)
    lava_coordinates = Coordinates(0, 0)
    test_world.add_lava(lava_coordinates)

    player = Player("emma")
    player_location = Coordinates(2,1)
    test_world.add_play_char(player, player_location, Direction.EAST)



    # Every Qt application must have one instance of QApplication.
    global app # Use global to prevent crashing on exit
    app = QApplication(sys.argv)
    gui = GUI(test_world, 50)

    # Start the Qt event loop. (i.e. make it possible to interact with the gui)
    sys.exit(app.exec())

    # Any code below this point will only be executed after the gui is closed.


if __name__ == "__main__":
    main()