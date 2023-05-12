class Square():
    """
    The class Square represents a single square.
    A square can contain either an obstacle. a player or it can be empty.
    """

    def __init__(self, is_tree=False, is_water=False, is_lava=False):

        self.play_char = None
        self.is_tree = is_tree
        self.is_water = is_water
        self.is_lava = is_lava


    def get_play_char(self):
        """
        Returns the playable character in the square and None if player not in square
        """
        return self.play_char

    def is_tree_square(self):
        """
        Returns a boolean value stating whether there is a tree in the square
        """
        return self.is_tree

    def is_water_square(self):
        """
        Returns a boolean value stating whether square is water
        """
        return self.is_water

    def is_lava_square(self):
        """
        Returns a boolean value stating whether square is lava
        """
        return self.is_lava


    def is_empty(self):
        """
        Returns a boolean value stating whether the square is empty
        """

        return not self.is_tree_square() and self.play_char is None


    def set_play_char(self, play_char):
        """
        Marks the square as containing a player, if possible.
        If the square was not empty, the method fails to do anything.

        Parameter robot is the robot to be placed in this square: Player

        Returns a boolean value indicating if the operation succeeded: boolean
        """
        if self.is_empty():
            self.play_char = play_char
            return True
        else:
            return False


    def remove_play_char(self):
        """
        Removes the character in this square.

        Returns the character removed from the square or None, if there was no character: Character
        """
        removed_char = self.get_play_char()
        self.play_char = None
        return removed_char


    def set_tree(self):
        """
        Sets a tree in this square, if possible.
        If the square was not empty, the method fails to do anything.

        Returns a boolean value indicating if the operation succeeded: boolean
        """
        if self.is_empty():
            self.is_tree = True
            return True
        else:
            return False

    def set_water(self):
        """
        Sets water in this square, if possible
        If the square was not empty, the method fails to do anything.

        Returns a boolean value indicating if the operation succeeded: boolean
        """
        if self.is_empty():
            self.is_water = True
            return True
        else:
            return False

    def set_lava(self):
        """
        Sets lava in this square, if possible.
        If the square was not empty, the method fails to do anything.

        Returns a boolean value indicating if the operation succeeded: boolean
        """
        if self.is_empty():
            self.is_lava = True
            return True
        else:
            return False
