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
            for j in range(len(self.to_grid[i])):
                if self.from_grid[i][j] != other.from_grid[i][j]:
                    return False
        return True

    def __str__(self):
        """

        Return a human-readable string representation of MNPuzzle self.
        :type self: MNPuzzle
        :rtype: str

        >>> target_grid = (("1", "2", "3"), ("4", "5", "*"))
        >>> start_grid = (("*", "2", "3"), ("1", "4", "5"))
        >>> mn = MNPuzzle(start_grid, target_grid)
        >>> print(mn)
        * 2 3
        1 4 5

        """

        result = ""
        for row in self.from_grid:
            for element in row:
                result += str(element)
                result += " "
            result = result.strip(" ")
            result += "\n"

        result = result.strip("\n")
        return result

    def __repr__(self):
        """

        :return:
        :rtype: str
        """

        result = "MNPuzzle(self, {}, {})".format(
            self.grid_string(self.from_grid),
            self.grid_string(self.to_grid))

        return result

    def extensions(self):
        """

        :return:
        :rtype:

        Return a list of extensions of MNPuzzle self.

        >>> target_grid = (("1", "2"), ("3", "*"))
        >>> start_grid = (("*", "2"), ("1", "3"))
        >>> mn = MNPuzzle(start_grid, target_grid)
        >>> L1 = [child.from_grid for child in mn.extensions()]
        >>> L2 = [(("2", "*"), ("1", "3")), (("1", "2"), ("*", "3"))]
        >>> len(L1) == len(L2)
        True
        >>> all([s in L2 for s in L1])
        True
        >>> all([s in L1 for s in L2])
        True
        >>> start_grid2 = (("1", "2", "3"), ("*", "5", "6"), ("7", "8", "9"))
        >>> target = ((" ", " ", " "), (" ", " ", " "), (" ", " ", " "))
        >>> example = MNPuzzle(start_grid2, target)
        >>> for ex in example.extensions(): print(ex, "END")
        * 2 3
        1 5 6
        7 8 9 END
        1 2 3
        5 * 6
        7 8 9 END
        1 2 3
        7 5 6
        * 8 9 END
        """

        extensions = []
        # A tuple for the location of the blank spot
        swap_spot = self.find_coordinates("*")
        directions = ["N", "E", "S", "W"]

        for direction in directions:
            # swap_direction() returns an mn puzzle that we can append
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
        >>> mn = MNPuzzle(start_grid, target_grid)
        >>> mn.is_solved()
        True
        >>> target_grid = (("1", "2"), ("3", "*"))
        >>> start_grid = (("*", "2"), ("1", "3"))
        >>> mn_2 = MNPuzzle(start_grid, target_grid)
        >>> mn_2.is_solved()
        False
        """

        # TODO
        # override is_solved
        # a configuration is solved when from_grid is the same as to_grid

        return self.from_grid == self.to_grid

    def grid_string(self, grid):
        """

        Return a string representation of the given grid

        @param MNPuzzle self: this MNPuzzle
        @param tuple[tuple[str]] grid: current configuration
        @rtype: str
        """

        result = ""
        for row in grid:
            for element in row:
                result += str(element)
                result += " "
            result += "\n"

        return result

    def swap_direction(self, origin, direction):
        """
        Return an MN puzzle where the object at origin is switched with the
        object in direction in its from_grid. If this is not possible, return
        None
        :type origin: list[int, int]
        :type direction: str
        :rtype: MNPuzzle
        >>> target_grid = (("1", "2", "3"), ("4", "5", "*"))
        >>> start_grid = (("*", "2", "3"), ("1", "4", "5"))
        >>> mn = MNPuzzle(start_grid, target_grid)
        >>> p = mn.swap_direction([0, 0], "E")
        >>> print(p)
        2 * 3
        1 4 5
        >>> start_grid2 = (("1", "2"), ("3", "*"))
        >>> target_grid2 = (("1", "*"), ("3", "2"))
        >>> mn2 = MNPuzzle(start_grid2, target_grid2)
        >>> p2 = mn2.swap_direction([1, 1], "N")
        >>> print(p2)
        1 *
        3 2
        """

        found = False
        starter_grid = turn_to_list(self.from_grid)

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
            if origin_column != len(starter_grid[0])-1:
                # Add 1 to the column coordinate to go 1 right
                origin_column += 1
                found = True

        elif direction == "S":
            # If it's not in the bottom row
            if not origin_row == len(starter_grid) - 1:
                # Subtract 1 from the row coordinate to go 1 down
                origin_row += 1
                found = True

        elif direction == "W":
            # If it's not in the leftmost column
            if origin_column != 0:
                # Subtract 1 from the column coordinate to go 1 left
                origin_column -= 1
                found = True
        if found:
            starter_grid[origin[1]][origin[0]], \
                starter_grid[origin_row][origin_column] = \
                starter_grid[origin_row][origin_column], \
                starter_grid[origin[1]][origin[0]]

            starter_grid = turn_to_tup(starter_grid)
            return MNPuzzle(starter_grid, self.to_grid)

        else:
            return None

    def find_coordinates(self, obj):
        """

        Return the position of the first occurrence of obj in self.from_grid

        :type obj: any
        :rtype: list[int, int] | str

        >>> target_grid = (("1", "2", "3"), ("4", "5", "*"))
        >>> start_grid = (("*", "2", "3"), ("1", "4", "5"))
        >>> mn = MNPuzzle(start_grid, target_grid)
        >>> mn.find_coordinates("*")
        [0, 0]
        """

        for i in range(self.n):
            for j in range(self.m):
                if self.from_grid[i][j] == obj:
                    return [j, i]

        return "error: object not in grid"


def turn_to_list(tup):
    """

    Return a possibly nested list from a possibly nested tuple given.

    :type tup: tuple(int, int) | Any
    :rtype: list[int, int]

    >>> t = ((1, 2),(3, 4))
    >>> cheryl = turn_to_list(t)
    >>> print(cheryl)
    [[1, 2], [3, 4]]
    """

    if isinstance(tup, tuple):
        return [turn_to_list(t) for t in tup]
    else:
        return tup


def turn_to_tup(list_):
    """
    Return a possibly nested tuple from a possibly nested list given.

    :type list_: list[list[int]] | Any
    :rtype: tuple(int, int)

    >>> y = [[1, 2], [3, 4]]
    >>> t = turn_to_tup(y)
    >>> print(t)
    ((1, 2), (3, 4))
    """

    if isinstance(list_, list):
        return tuple(turn_to_tup(i) for i in list_)
    else:
        return list_

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
