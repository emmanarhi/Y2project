class Direction():
    """
    These constants represent the main
    compass directions that robots can move in.
    """
    NORTH = (0, -1)
    EAST = (1, 0)
    SOUTH = (0, 1)
    WEST = (-1, 0)

    @staticmethod
    def get_x_step(facing):
        """
        Returns the change of the x coordinate if moving one "step"
        in the direction represented by the given compass direction.
        E.g. for C{WEST} the "x step" is
        -1 since moving one step west means a decrease of one in
        the x coordinate.

        Returns: -1, 0 or 1

        See the documentation of class Coordinates
        """
        return facing[0]


    @staticmethod
    def get_y_step(facing):
        """
        Returns the change of the y coordinate if moving one
        "step" in the direction represented by by the given compass
        direction. E.g. for C{NORTH} the "y step" is
        -1 since moving one step north means a decrease of one in
        the y coordinate.

        Returns: -1, 0 or 1

        See the documentation of class Coordinates
        """
        return facing[1]

    @staticmethod
    def get_values():
        """
        Creates a list of directions in a clockwise direction starting
        from north.

        Returns: list of direction tuples
        """
        return [Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST]