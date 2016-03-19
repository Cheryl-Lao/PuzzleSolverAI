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

        :return:
        :rtype: str
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
        """

        extensions = []
        # A tuple for the location of the
        swap_spot = self.find_coordinates("*")

        commands = ["swap_spot[0] += 1", "swap_spot[0] -= 1",
                    "swap_spot[1] += 1", "swap_spot[1] -= 1"]

        for command in commands:

            copied_grid = self[:]
            eval(command)
            new_spot = swap_spot
            copied_grid.swap_positions(copied_grid.m, copied_grid.n, new_spot[0], new_spot[1])

            if copied_grid is not None:
                extensions.append(copied_grid)

    def is_solved(self):
        """

        :return:
        :rtype:
        """

        # TODO
        # override is_solved
        # a configuration is solved when from_grid is the same as to_grid

        return self.from_grid == self.to_grid

    def swap_positions(self, x1, y1, x2, y2):
        """
        Return an MN puzzle where the object at (x1, y1) is switched with the
        object at (x2, y2) in its from_grid. If this is not possible, return
        None

        :type x1:int
        :type y1:int
        :type x2: int
        :type y2: int
        :rtype: MNPuzzle
        """

        starter_grid = list(self.from_grid)[:]
        max_x = self.m - 1
        max_y = self.n - 1

        if x1 >= max_x or y1>= max_y or x2 >= max_x or y2 >= max_y:
            return None

        starter_grid[x1][y1] , starter_grid[x2][y2] = \
            starter_grid[x2][y2], starter_grid[x1][y1]

        starter_grid = tuple(starter_grid)

        return MNPuzzle(starter_grid, self.to_grid)

    def find_coordinates(self, obj):
        """

        :param obj:
        :type obj:
        :return:
        :rtype:
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
