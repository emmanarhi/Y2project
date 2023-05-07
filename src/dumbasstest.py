import os
def read_map_file(file_name):
    try:
        file = open(file_name, "r")
        row = file.readline().lower()
        print(row)

        if "world" in row:
            if file.readline().lower == "trees":
                tree_coords = file.readline().split(",")
                print(tree_coords)
    except OSError:
        print("fuckshit")


def main():
    read_map_file("hah.txt")
    return 1
