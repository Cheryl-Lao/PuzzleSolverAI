"""
Some functions for working with puzzles
"""
from puzzle import Puzzle
from collections import deque
# set higher recursion limit
# which is needed in PuzzleNode.__str__
#import resource
import sys
#resource.setrlimit(resource.RLIMIT_STACK, (2**29, -1))
sys.setrecursionlimit(10**6)

def gather_lists(list_):
    """
    Return the concatenation of the sublists of list_.

    @param list[list] list_: list of sublists
    @rtype: list

    Algorithm from answer on http://stackoverflow.com/questions/12472338/flattening-a-list-recursively

    >>> list_ = [[1, 2], [3, 4]]
    >>> gather_lists(list_)
    [1, 2, 3, 4]
    """
    if list_ == []:
        return list_
    if isinstance(list_[0], list):
        return (gather_lists(list_[0]) + gather_lists(list_[1:]))

    return (list_[:1] + list_[1:])

# TODO
# implement depth_first_solve
# do NOT change the type contract
# you are welcome to create any helper functions
# you like
def depth_first_solve(puzzle):
    """
    Return a path from PuzzleNode(puzzle) to a PuzzleNode containing
    a solution, with each child containing an extension of the puzzle
    in its parent.  Return None if this is not possible.

    @type puzzle: Puzzle
    @rtype: PuzzleNode | None
    """

    seen = set()

    return depth_helper(puzzle, seen)


def depth_helper(puzzle, seen):
    """
    :param puzzle: Puzzle
    :param seen: Set
    :return: Puzzle | None
    """

    seen.add(puzzle)

    if puzzle.is_solved():
            return puzzle

    elif puzzle.fail_fast():
        return None

    if puzzle.extensions():
        # Look for solutions in each branch
        for child in puzzle.extensions():
            # This will return the first leaf that is not None
            # (so it's a solution) and exit the loop
            if depth_helper(child, seen) is not None and child not in seen:
                return depth_helper(child, seen)
    else:
        if puzzle.is_solved():
            return puzzle
        else:
            return None


def breadth_first_solve(puzzle):
    """
    Return a path from PuzzleNode(puzzle) to a PuzzleNode containing
    a solution, with each child PuzzleNode containing an extension
    of the puzzle in its parent.  Return None if this is not possible.

    @type puzzle: Puzzle
    @rtype: PuzzleNode


# implement breadth_first_solve
# do NOT change the type contract
# you are welcome to create any helper functions
# you like
# Hint: you may find a queue useful, that's why
# we imported deque
    """
    # TODO
    to_check = deque()
    to_check.add(puzzle)
    seen = set()

    while to_check:
        puzzle_config = to_check.pop(0)
        if puzzle_config.fail_fast():
            return None
        if puzzle_config not in seen:
            # Check if the puzzle configuration is a solution
            # and return it straight away if it is
            if puzzle_config.is_solved():
                return puzzle_config

            if puzzle_config.extensions:
                # If there are extensions add the children all at once to the queue
                for extension in puzzle_config.extensions:
                    to_check.add(extension)
            seen.add(puzzle_config)
    # If it gets to this line it means that there were no solutions found at all
    return None

# Class PuzzleNode helps build trees of PuzzleNodes that have
# an arbitrary number of children, and a parent.


class PuzzleNode:
    """
    A Puzzle configuration that refers to other configurations that it
    can be extended to.
    """

    def __init__(self, puzzle=None, children=None, parent=None):
        """
        Create a new puzzle node self with configuration puzzle.

        @type self: PuzzleNode
        @type puzzle: Puzzle | None
        @type children: list[PuzzleNode]
        @type parent: PuzzleNode | None
        @rtype: None
        """
        self.puzzle, self.parent = puzzle, parent
        if children is None:
            self.children = []
        else:
            self.children = children[:]

    def __eq__(self, other):
        """
        Return whether Puzzle self is equivalent to other

        @type self: PuzzleNode
        @type other: PuzzleNode | Any
        @rtype: bool

        >>> from word_ladder_puzzle import WordLadderPuzzle
        >>> pn1 = PuzzleNode(WordLadderPuzzle("on", "no", {"on", "no", "oo"}))
        >>> pn2 = PuzzleNode(WordLadderPuzzle("on", "no", {"on", "oo", "no"}))
        >>> pn3 = PuzzleNode(WordLadderPuzzle("no", "on", {"on", "no", "oo"}))
        >>> pn1.__eq__(pn2)
        False
        >>> pn1.__eq__(pn3)
        False
        """
        return (type(self) == type(other) and
                self.puzzle == other.puzzle and
                all([x in self.children for x in other.children]) and
                all([x in other.children for x in self.children]))

    def __str__(self):
        """
        Return a human-readable string representing PuzzleNode self.

        # doctest not feasible.
        """
        return "{}\n\n{}".format(self.puzzle,
                                 "\n".join([str(x) for x in self.children]))
