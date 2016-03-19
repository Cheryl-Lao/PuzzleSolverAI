from puzzle import Puzzle


class GridPegSolitairePuzzle(Puzzle):
    """
    Snapshot of peg solitaire on a rectangular grid. May be solved,
    unsolved, or even unsolvable.
    """

    def __init__(self, marker, marker_set):
        """
        Create a new GridPegSolitairePuzzle self with
        marker indicating pegs, spaces, and unused
        and marker_set indicating allowed markers.

        @type marker: list[list[str]]
        @type marker_set: set[str]
                          "#" for unused, "*" for peg, "." for empty
        """
        assert isinstance(marker, list)
        assert len(marker) > 0
        assert all([len(x) == len(marker[0]) for x in marker[1:]])
        assert all([all(x in marker_set for x in row) for row in marker])
        assert all([x == "*" or x == "." or x == "#" for x in marker_set])
        self._marker, self._marker_set = marker, marker_set

    # TODO
    # implement __eq__, __str__ methods
    # __repr__ is up to you

    def extensions(self):
        marker, marker_set = self._marker, self._marker_set

        pegs = {}  # dictionary of tuples representing pegs on board,
        # each with a list of directions

        for i in range(len(marker)): # finds the pegs
            for j in range(len(marker[i])):
                if marker[i][j] == "*":
                    pegs[(i, j)] = []

        for p in pegs: # for each peg, find movable directions

            if p[1] - 2 >= 0 and marker[p[0]][p[1] - 1] == "*" and marker[p[0]][p[1] - 2] == ".":
                pegs[p].append("left")  # peg can move left

            if p[1] + 2 < len(marker[0]) and marker[p[0]][p[1] + 1] == "*" and marker[p[0]][p[1] + 2] == ".":
                pegs[p].append("right")  # peg can move right

            if p[0] - 2 >= 0 and marker[p[0] - 1][p[1]] == "*" and marker[p[0] - 2][p[1] - 2] == ".":
                pegs[p].append("up")  # peg can move up

            if p[0] + 2 < len(marker) and marker[p[0] + 1][p[1]] == "*" and marker[p[0] + 2][p[1] - 2] == ".":
                pegs[p].append("down")  # peg can move down

        charts = [self.create_new_grid(p, d) for p in pegs for d in pegs[p]]

        return [GridPegSolitairePuzzle(c, marker_set) for c in charts]


    # TODO
    # override extensions
    # legal extensions consist of all configurations that can be reached by
    # making a single jump from this configuration

    def create_new_grid(self, coord, direction):
        chart = self._marker

        if direction == "left":
            chart[coord[0]][coord[0]] = "."  # jumping peg's spot is emptied
            chart[coord[0]][coord[1] - 1] = "."  # emptied
            chart[coord[0]][coord[1] - 2] = "*"  # peg moves here

        elif direction == "right":
            chart[coord[0]][coord[0]] = "."  # jumping peg's spot is emptied
            chart[coord[0]][coord[1] + 1] = "."  # emptied
            chart[coord[0]][coord[1] + 2] = "*"  # peg moves here

        elif direction == "up":
            chart[coord[0]][coord[0]] = "."  # jumping peg's spot is emptied
            chart[coord[0] - 1][coord[1]] = "."  # emptied
            chart[coord[0] - 2][coord[1]] = "*"  # peg moves here

        elif direction == "down":
            chart[coord[0]][coord[0]] = "."  # jumping peg's spot is emptied
            chart[coord[0] + 1][coord[1]] = "."  # emptied
            chart[coord[0] + 2][coord[1]] = "*"  # peg moves here

        return chart

    def is_solved(self):
        # TODO
        # override is_solved
        # A configuration is solved when there is exactly one "*" left
        pegs = sum([x.count("*") for x in self._marker])
        # Total "*" for row in board
        return pegs == 1

    def __str__(self):
        """

        :return:
        :rtype: str
        """

        return "\n".join(x for x in self._marker)

    def __eq__(self, other):
        """

        :type other: GridPegSolitairePuzzle
        :rtype: bool
        """

        if self.marker_set != other.marker_set:
            return False

        for i in range(len(self.marker)):
            for j in range(len(self.marker[i])):
                if self.marker[i][j] != other.marker[i][j]:
                    return False

        return True

    def __repr__(self):
        """

        Return a string representation of self that can be used by
        :return:
        :rtype: str
        """
        marker_string = Puzzle.grid_string(self.marker)
        marker_set = str(self.marker_set)

        return "GridPegSolitairePuzzle(marker, marker_set)".format(marker_string)

if __name__ == "__main__":
    import doctest

    doctest.testmod()
    from puzzle_tools import depth_first_solve

    grid = [["*", "*", "*", "*", "*"],
            ["*", "*", "*", "*", "*"],
            ["*", "*", "*", "*", "*"],
            ["*", "*", ".", "*", "*"],
            ["*", "*", "*", "*", "*"]]
    gpsp = GridPegSolitairePuzzle(grid, {"*", ".", "#"})
    import time

    start = time.time()
    solution = depth_first_solve(gpsp)
    end = time.time()
    print("Solved 5x5 peg solitaire in {} seconds.".format(end - start))
    print("Using depth-first: \n{}".format(solution))
