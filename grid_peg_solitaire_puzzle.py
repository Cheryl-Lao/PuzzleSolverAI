from puzzle import Puzzle
import copy

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

    # TODO
    # override extensions
    # legal extensions consist of all configurations that can be reached by
    # making a single jump from this configuration
    def extensions(self):
        """
        Return a list of legal GridPegSolitairePuzzle extensions from self

        :rtype: list[GridPegSolitairePuzzle]

        >>> grid = [["*", "*", "*", "*", "*"], \
                   ["*", "*", "*", "*", "*"], \
                   ["*", "*", "*", "*", "*"], \
                   ["*", "*", ".", "*", "*"], \
                   ["*", "*", "*", "*", "*"]]
        >>> sample = GridPegSolitairePuzzle(grid, {"*", ".", "#"})
        >>> for sample in sample.extensions(): print(sample, "END")
        * * * * *
        * * . * *
        * * . * *
        * * * * *
        * * * * * END
        * * * * *
        * * * * *
        * * * * *
        * * * . .
        * * * * * END
        * * * * *
        * * * * *
        * * * * *
        . . * * *
        * * * * * END
        >>> grid2 = [[".", "*", "*", "*", "*"], \
                   ["*", "*", "*", "*", "*"], \
                   ["*", "*", "*", "*", "*"], \
                   ["*", "*", "*", "*", "*"], \
                   ["*", "*", "*", "*", "*"]]
        >>> sample2 = GridPegSolitairePuzzle(grid2, {"*", ".", "#"})
        >>> for sample in sample2.extensions(): print(sample, "END")
        * . . * *
        * * * * *
        * * * * *
        * * * * *
        * * * * * END
        * * * * *
        . * * * *
        . * * * *
        * * * * *
        * * * * * END
        >>> grid3 = [["#", "*"], \
                   ["#", "#"], \
                   [".", "*"], \
                   ["*", "*"], \
                   ["*", "*"]]
        >>> sample3 = GridPegSolitairePuzzle(grid3, {"*", ".", "#"})
        >>> for sample in sample3.extensions(): print(sample, "END")
        # *
        # #
        * *
        . *
        . * END
        >>> grid4 = [["#", "*"], \
                   ["#", "#"]]
        >>> sample4 = GridPegSolitairePuzzle(grid4, {"*", ".", "#"})
        >>> for sample in sample4.extensions(): print(sample, "END")

        """

        result = []
        empty_spaces = self.list_empty_spaces()
        directions = ["N", "E", "S", "W"]
        copied = copy.deepcopy(self)

        for origin in empty_spaces:

            for direction in directions:
                neighbour = copied.neighbour_at(origin, direction)

                if neighbour is not None and neighbour[1] != "#":
                    next_neighbour = copied.neighbour_at(neighbour[0],direction)

                    if next_neighbour is not None and next_neighbour[1] != "#":
                        # Peg fills up the empty spot
                        copied._marker[origin[1]][origin[0]] = "*"
                        # Peg that is skipped over is taken off
                        copied._marker[neighbour[0][1]][neighbour[0][0]] = "."
                        # Peg's original location is now empty
                        copied._marker[next_neighbour[0][1]]\
                            [next_neighbour[0][0]] = "."

                        result.append(copied)
                # Reset copied
                copied = copy.deepcopy(self)
        return result

    def list_empty_spaces(self):
        """

        Return a list of coordinates for the empty spaces in self

        :rtype: list[tuple(int, int)]

        >>> grid = [[".", "*", "*", "*", "*"], \
                   ["*", "*", "*", "*", "*"], \
                   ["*", "*", "*", "*", "*"], \
                   ["*", "*", ".", "*", "*"], \
                   ["*", "*", "*", "*", "."]]
        >>> sample = GridPegSolitairePuzzle(grid, {"*", ".", "#"})
        >>> sample.list_empty_spaces()
        [(0, 0), (2, 3), (4, 4)]
        >>> grid2 = [["*", "*", "*", "*", "*"], \
                   ["*", "*", "*", "*", "*"], \
                   ["#", "*", "#", "*", "*"], \
                   ["*", "*", "*", "*", "*"], \
                   ["*", "*", "*", "*", "#"]]
        >>> sample2 = GridPegSolitairePuzzle(grid2, {"*", ".", "#"})
        >>> sample2.list_empty_spaces()
        []
        """

        empty_spaces = []

        for i in range(len(self._marker[0])):
            for j in range((len(self._marker))):
                if self._marker[j][i] == ".":
                    empty_spaces.append((i, j))
        return empty_spaces

    def neighbour_at(self, origin, direction):
        """

        Return a tuple of the location and symbol of the peg in direction of
        origin if it exists. Otherwise, return None

        :type origin: tuple(int, int)
        :type direction: str
        :rtype: tuple(tuple(int, int), str) | None

        >>> grid = [["*", "*", "*", "*", "*"], \
                   ["*", "*", "*", "*", "*"], \
                   ["#", "*", "#", "*", "*"], \
                   ["*", "*", "*", "*", "*"], \
                   ["*", "*", "*", "*", "#"]]
        >>> sample = GridPegSolitairePuzzle(grid, {"*", ".", "#"})
        >>> sample.neighbour_at((2, 1), "S")
        ((2, 2), '#')
        """

        # Origin_row is the y-coord of the coordinate which is the row number
        origin_row = origin[1]
        # Origin_column is the x-coord of the coordinate which is the row number
        origin_column = origin[0]
        # Keeping track of whether or not the coordinate was found
        found = False

        if direction == "N":
            # If it's not on the top row
            if origin_row != 0:
                # Subtract 1 from the n coordinate to go 1 up
                origin_row -= 1
                found = True

        elif direction == "E":
            # If it's not in the rightmost column
            if origin_column != len(self._marker[0])-1:
                # Add 1 to the column coordinate to go 1 right
                origin_column += 1
                found = True

        elif direction == "S":
            # If it's not in the bottom row
            if not origin_row == len(self._marker) - 1:

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
            neighbour_coord = (origin_column, origin_row)
            # Find the symbol at the changed coordinates
            neighbour_symbol = self._marker[origin_row][origin_column]
            # Return the neighbour's location and symbol

            return neighbour_coord, neighbour_symbol

        else:
            return None

    def fail_fast(self):
        """

        Return whether or not a GridPegSolitairePuzzle is unsolvable

        :return:
        :rtype: bool
        """

        if not self.extensions():
            return True

        return False

    def is_solved(self):
        """
        Return whether or not a GridPegPuzzle is in a solved state

        :rtype: bool

        >>> grid = [["#", "*", "*", "*", "*"],\
                   ["*", "*", "*", ".", "*"],\
                   [".", "*", "*", "*", "*"],\
                   ["*", "#", ".", "*", "*"],\
                   ["*", ".", "*", "*", "*"]]
        >>> example = GridPegSolitairePuzzle(grid, {"*", ".", "#"})
        >>> example.is_solved()
        False
        >>> did_grid = [[".", "*", ".", ".", "."],\
                       [".", ".", ".", ".", "."],\
                       [".", "#", ".", ".", "."],\
                       [".", ".", ".", ".", "#"],\
                       [".", ".", ".", ".", "."]]
        >>> example2 = GridPegSolitairePuzzle(did_grid, {"*", ".", "#"})
        >>> example2.is_solved()
        True
        """

        # TODO
        # override is_solved
        # A configuration is solved when there is exactly one "*" left
        pegs = sum([x.count("*") for x in self._marker])
        # Total "*" for row in board
        return pegs == 1

    def __str__(self):
        """
        Return  string representation of a GridPegSolitairePuzzle

        :rtype: str

        >>> grid = [["#", "*", "*", "*", "*"],\
                   ["*", "*", "*", ".", "*"],\
                   [".", "*", "*", "*", "*"],\
                   ["*", "#", ".", "*", "*"],\
                   ["*", ".", "*", "*", "*"]]
        >>> example = GridPegSolitairePuzzle(grid, {"*", ".", "#"})
        >>> print(example)
        # * * * *
        * * * . *
        . * * * *
        * # . * *
        * . * * *

        >>> grid2 = [[".", "#"],\
                     ["*", "*"],\
                     [".", "*"],\
                     ["*", "#"],\
                     ["*", "."]]
        >>> example2 = GridPegSolitairePuzzle(grid2, {"*", ".", "#"})
        >>> print(example2)
        . #
        * *
        . *
        * #
        * .
        """

        result = ""
        # Loop through each row
        for i in range(len(self._marker)):
            # Each element in each row
            for j in range(len(self._marker[0])):
                result += str(self._marker[i][j])
                result += " "
            # Take off the extra blank space - we aren't Taylor Swift
            result = result.strip(" ")
            result += "\n"

        result = result.strip("\n")
        return result

    def __eq__(self, other):
        """
        Return whether or not two GridPegSolitairePuzzles are equal

        :type other: GridPegSolitairePuzzle
        :rtype: bool

        >>> grid = [["#", "*", "*", "*", "*"],\
                   ["*", "*", "*", ".", "*"],\
                   [".", "*", "*", "*", "*"],\
                   ["*", "#", ".", "*", "*"],\
                   ["*", ".", "*", "*", "*"]]
        >>> pegitaire = GridPegSolitairePuzzle(grid, {"*", ".", "#"})
        >>> grid2= [["#", "*", "*", "*", "*"],\
                   ["*", "*", "*", ".", "*"],\
                   [".", "*", "*", "*", "*"],\
                   ["*", "#", ".", "*", "*"],\
                   ["*", ".", "*", "*", "*"]]
        >>> identical_twin = GridPegSolitairePuzzle(grid2, {"*", ".", "#"})
        >>> pegitaire == identical_twin
        True
        >>> grid3= [["*", "*", "*", "*", "*"],\
                   ["*", "*", "*", "*", "*"],\
                   ["*", "*", "*", "*", "*"],\
                   ["*", "*", "*", "*", "*"],\
                   ["*", "*", "*", "*", "*"]]
        >>> fraternal_twin = GridPegSolitairePuzzle(grid3,{"*", ".", "#"})
        >>> pegitaire == fraternal_twin
        False
        """

        for i in range(len(self._marker)):
            for j in range(len(self._marker[i])):
                if self._marker[i][j] != other._marker[i][j]:
                    return False

        return True

    def __repr__(self):
        """

        Return a string representation of self that can be used by the
        initializer.

        :rtype: str

        >>> grid = [["#", "*", "*", "*", "*"],\
                   ["*", "*", "*", ".", "*"],\
                   [".", "*", "*", "*", "*"],\
                   ["*", "#", ".", "*", "*"],\
                   ["*", ".", "*", "*", "*"]]
        >>> example = GridPegSolitairePuzzle(grid, {"*", ".", "#"})
        >>> example.__repr__()
        "GridPegSolitairePuzzle([['#', '*', '*', '*', '*'], ['*', '*', '*', '.', '*'], ['.', '*', '*', '*', '*'], ['*', '#', '.', '*', '*'], ['*', '.', '*', '*', '*']], {'.', '*', '#'})"
        """

        marker_string = str(self._marker)
        marker_set = str(self._marker_set)

        return "GridPegSolitairePuzzle({}, {})".format(marker_string,marker_set)


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
