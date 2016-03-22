from puzzle import Puzzle


class MNPuzzle(Puzzle):
    """
    An nxm puzzle, like the 15-puzzle, which may be solved, unsolved,
    or even unsolvable.
    """

    def __init__(self, from_grid, to_grid):
        """
        MNPuzzle in state from_grid, working towards
        state to_grid

        @param MNPuzzle self: this MNPuzzle
        @param tuple[tuple[str]] from_grid: current configuration
        @param tuple[tuple[str]] to_grid: solution configuration
        @rtype: None
        """
        # represent grid symbols with letters or numerals
        # represent the empty space with a "*"
        assert len(from_grid) > 0
        assert all([len(r) == len(from_grid[0]) for r in from_grid])
        assert all([len(r) == len(to_grid[0]) for r in to_grid])
        self.n, self.m = len(from_grid), len(from_grid[0])
        self.from_grid, self.to_grid = from_grid, to_grid

    # TODO
    # implement __eq__ and __str__
    # __repr__ is up to you
    def __eq__(self, other):
        """

        Precondition: self and other are both rectangular grids

        :rtype: str

        >>> grid_1 = (("1", "2", "3"), ("4", "5", "*"))
        >>> grid_2 = (("1", "2", "3"), ("4", "5", "*"))
        >>> grid_3 = (("1", "2", "3"), ("4", "5", "*"), ("6", "7", "8"))
        >>> grid_1.__eq__(grid_2)
        True
        >>> grid_1.__eq__(grid_3)
        False
        """

        if len(self.to_grid) != len(other.to_grid):
            return False

        for i in range(len(self.from_grid)):
            for j in range (len(self.to_grid[i])):
                if self.from_grid[i][j] != other.from_grid[i][j]:
                    return False
        return True

    def __str__(self):
        """

        :return:
        :rtype: str
        Return a human-readable string representation of MNPuzzle self.

        >>> target_grid = (("1", "2", "3"), ("4", "5", "*"))
        >>> start_grid = (("*", "2", "3"), ("1", "4", "5"))
        >>> mn = MNPuzzle(start_grid, target_grid))
        >>> print(mn)
        1 2 3
        4 5 *
        """

        result = ""
        for row in self.to_grid:
            for element in row:
                result += str(element)
                result += " "
            result += "\n"

        return result

    def __repr__(self):
        """

        :return:
        :rtype: str
        """

        result = "MNPuzzle(self, {}, {})".format(Puzzle.grid_string(self.from_grid), Puzzle.grid_string(self.to_grid))

        return result

    def extensions(self):
        """

        :return:
        :rtype:

        Return a list of extensions of MNPuzzle self.

        >>> target_grid = (("1", "2"), ("3", "*"))
        >>> start_grid = (("*", "2"), ("1", "3"))
        >>> mn = MNPuzzle(start_grid, target_grid))
        >>> L1 = list(mn.extensions())
        >>> L2 = [(("2", "*"), ("1", "3")), (("1", "2"), ("*", "3"))]
        >>> len(L1) == len(L2)
        >>> all([s in L2 for s in L1])
        True
        >>> all([s in L1 for s in L2])
        True
        """

        extensions = []
        # A tuple for the location of the blank spot
        swap_spot = self.find_coordinates("*")
        directions = ["N", "E", "S", "W"]

        for direction in directions:

            new_grid = self.swap_direction(swap_spot, direction)

            if new_grid is not None:
                extensions.append(new_grid)
        return extensions

    def is_solved(self):
        """

        :return:
        :rtype: bool
        Return whether Puzzle self is solved.

        >>> target_grid = (("*", "2"), ("1", "3"))
        >>> start_grid = (("*", "2"), ("1", "3"))
        >>> mn = MNPuzzle(start_grid, target_grid))
        >>> mn.is_solved()
        True
        >>> target_grid = (("1", "2"), ("3", "*"))
        >>> start_grid = (("*", "2"), ("1", "3"))
        >>> mn_2 = MNPuzzle(start_grid, target_grid))
        >>> mn_2.is_solved()
        False
        """

        # TODO
        # override is_solved
        # a configuration is solved when from_grid is the same as to_grid

        return self.from_grid == self.to_grid

    def swap_direction(self, origin, direction):
        """
        Return an MN puzzle where the object at origin is switched with the
        object in direction in its from_grid. If this is not possible, return
        None
        :type origin: tuple(int, int)
        :type str
        :rtype: MNPuzzle


        """

        starter_grid = list(self.from_grid)
        origin_row = origin[1]
        origin_column = origin[0]



        if direction == "N":
            # If it's not on the top row
            if origin_row != 0:
                # Subtract 1 from the n coordinate to go 1 up
                origin_row -= 1
                found = True

        elif direction == "E":
            # If it's not in the rightmost column
            if origin_column != len(self.from_grid[0])-1:
                # Add 1 to the column coordinate to go 1 right
                origin_column += 1
                found = True

        elif direction == "S":
            # If it's not in the bottom row
            if not origin_row == len(self.from_grid) - 1:

                # Subtract 1 from the row coordinate to go 1 down
                origin_row += 1
                found = True

        elif direction == "W":
            # If it's not in the leftmost column
            if origin_column != 0:
                # Subtract 1 from the column coordinate to go 1 left
                origin_column -= 1
                found = True


        starter_grid[pos1[0]][pos1[1]] , starter_grid[pos2[0]][pos2[1]] = \
            starter_grid[pos2[0]][pos2[1]], starter_grid[pos1[0]][pos1[1]]

        starter_grid = tuple(starter_grid)

        return MNPuzzle(starter_grid, self.to_grid)

    def find_coordinates(self, obj):
        """

        :param obj:
        :type obj:
        :return:
        :rtype:

        >>> target_grid = (("1", "2", "3"), ("4", "5", "*"))
        >>> start_grid = (("*", "2", "3"), ("1", "4", "5"))
        >>> mn = MNPuzzle(start_grid, target_grid))
        >>> mn.find_coordinates(self, "*")
        [0, 0]
        """
        for i in range (self.m):
            for j in range (self.n):
                if self.from_grid[i][j] == obj:
                    return [i, j]
        return "error: object not in grid"

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    target_grid = (("1", "2", "3"), ("4", "5", "*"))
    start_grid = (("*", "2", "3"), ("1", "4", "5"))
    from puzzle_tools import breadth_first_solve, depth_first_solve
    from time import time
    start = time()
    solution = breadth_first_solve(MNPuzzle(start_grid, target_grid))
    end = time()
    print("BFS solved: \n\n{} \n\nin {} seconds".format(
        solution, end - start))
    start = time()
    solution = depth_first_solve((MNPuzzle(start_grid, target_grid)))
    end = time()
    print("DFS solved: \n\n{} \n\nin {} seconds".format(
        solution, end - start))
