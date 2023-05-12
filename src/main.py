import sys

from src.gameworld import *
from src.coordinates import *
from character import *
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget
from gui import *


def read_map_file(filename, world_num):
    try:
        file = open(filename, "r")
        row = file.readline().lower().rstrip()
        world_found = False

        while not world_found and row != "":
            if "world" in row and str(world_num) in row:
                world_found = True
            else:
                row = file.readline().lower().rstrip()

        row = file.readline().lower().rstrip()

        while "world" not in row and row != "":
            if world_num != 3:
                if "trees" in row:
                    tree_row = row.split(":")
                    tree_coords = tree_row[1].split(";")
                    tree_list = []
                    for i in range(len(tree_coords)):
                        coords = tree_coords[i].split(",")
                        coordinates = Coordinates(int(coords[0]), int(coords[1]))
                        tree_list.append(coordinates)
                elif "water" in row:
                    water_row = row.split(":")
                    water_coords = water_row[1].split(";")
                    water_list = []
                    for i in range(len(water_coords)):
                        coords = water_coords[i].split(",")
                        coordinates = Coordinates(int(coords[0]), int(coords[1]))
                        water_list.append(coordinates)
                elif "lava" in row:
                    lava_row = row.split(":")
                    lava_coords = lava_row[1].split(";")
                    lava_list = []
                    for i in range(len(lava_coords)):
                        coords = lava_coords[i].split(",")
                        coordinates = Coordinates(int(coords[0]), int(coords[1]))
                        lava_list.append(coordinates)
            if "size" in row:
                size_row = row.split(":")
                size_x, size_y = size_row[1].split(",")
            row = file.readline().lower().rstrip()

        file.close()

        if world_found and world_num != 3:
            return tree_list, water_list, lava_list, int(size_x), int(size_y)
        elif world_num == 3:
            return int(size_x), int(size_y)
        else:
            return 0

    except OSError:
        print("Couldn't open file")


def load_attacks(filename):
    try:
        file = open(filename, "r")
        attacks = {}
        row = file.readline().lower().rstrip()

        while row != "":
            attack_name, damage, attack_range = row.split(",")
            attacks[attack_name] = (int(damage), int(attack_range))
            row = file.readline().lower().rstrip()

        file.close()
        return attacks

    except OSError:
        print("Couldn't open file")


# Nyt valitettavasti laitan vaa pelaajat hard coded in koska aina sama layout
def load_map(filename, world_num):
    coordinates = read_map_file(filename, world_num)

    if world_num != 3:
        world = GameWorld(coordinates[3], coordinates[4])
        for tree in coordinates[0]:
            world.add_tree(tree)
        for water in coordinates[1]:
            world.add_water(water)
        for lava in coordinates[2]:
            world.add_lava(lava)
    else:
        world = GameWorld(coordinates[0], coordinates[1])

    # asetetaan eri hyökkäystyypit hahmoille, niiden nimessä aina hahmotyypin nimi
    attacks = load_attacks("C:/Users/enarh/PycharmProjects/Y2/projectgit/doc/attacks.txt")
    normal_attacks = attacks.copy()
    shooter_attacks = attacks.copy()
    tank_attacks = attacks.copy()
    for key, value in attacks.items():
        if "normal" not in key:
            del normal_attacks[key]
    for key, value in attacks.items():
        if "shoot" not in key:
            del shooter_attacks[key]
    for key, value in attacks.items():
        if "tank" not in key:
            del tank_attacks[key]

    player = Character("normal", False)
    player.attacks = normal_attacks

    player_2 = Character("shooter", False)
    player_2.attacks = shooter_attacks

    player_3 = Character("tank", False)
    player_3.attacks = tank_attacks

    enemy = Character("normal", True)
    enemy.attacks = normal_attacks
    enemy.add_ai()

    enemy_2 = Character("shooter", True)
    enemy_2.attacks = shooter_attacks
    enemy_2.add_ai()

    enemy_3 = Character("tank", True)
    enemy_3.attacks = tank_attacks
    enemy_3.add_ai()

    world.add_play_char(player, Coordinates(1, 3), Direction.EAST)
    world.add_play_char(player_2, Coordinates(1, 4), Direction.EAST)
    world.add_play_char(player_3, Coordinates(1, 5), Direction.EAST)

    world.add_enemy(enemy, Coordinates(13, 3), Direction.WEST)
    world.add_enemy(enemy_2, Coordinates(13, 4), Direction.WEST)
    world.add_enemy(enemy_3, Coordinates(13, 5), Direction.WEST)
    return world


def main():
    global app  # Use global to prevent crashing on exit
    app = QApplication(sys.argv)
    gui = GUI(50)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
