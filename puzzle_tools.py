"""
Some functions for working with puzzles
"""
from puzzle import Puzzle
from collections import deque
from grid_peg_solitaire_puzzle import *  # TODO REMOVE THESE IMPORTS AFTER TESTING
from word_ladder_puzzle import *
# set higher recursion limit
# which is needed in PuzzleNode.__str__
# import resource
import sys
# resource.setrlimit(resource.RLIMIT_STACK, (2**29, -1))
sys.setrecursionlimit(10**6)

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

    >>> tester1 = WordLadderPuzzle("cast", "vase", {"case", "cast", "vase"})
    >>> depth_first_solve(tester1)
    "PLEASE AT LEAST DO SOMETHING"

    >>> tester = GridPegSolitairePuzzle([[".", ".", "."], ["*", "*", "."],\
                                        ["*", "*", "."]], {".", "#", "*"})
    >>> depth_first_solve(tester)
    "I'M PRAYING RIGHT NOW"
    """

    seen = set()
    # This is the solution. I'm going backwards to construct a linked list
    # of PuzzleNodes where the returned node and all of its children only
    # have one child, eventually leading to the solution
    stop = []
    solution_node = depth_helper(puzzle, seen, stop)

    if solution_node:
        # Going backwards in the linked list to make
        while solution_node.parent:
            solution_node.parent.children = [solution_node.puzzle]
            solution_node = solution_node.parent

        # Making the top node's children only point in the path of the solution
        solution_node.parent.children = [solution_node]
        return solution_node.parent

    else:
        return None


def depth_helper(puzzle, seen, stop_it):
    """
    :param puzzle: Puzzle
    :param seen: set[str]
    :param stop_it: list[bool]
    :return: PuzzleNode | None
    """

    if stop_it:
        return None

    new_puzzle_node = PuzzleNode(puzzle)

    # So that we don't visit this configuration again
    seen.add(str(new_puzzle_node.puzzle))

    # Base Cases vvv
    if new_puzzle_node.puzzle.is_solved():
        stop_it .append(True)
        return new_puzzle_node

    elif new_puzzle_node.puzzle.fail_fast():
        return None
    # Base Cases ^^^

    temp_children = puzzle.extensions()
    new_puzzle_node.children = []

    # Since failfast checks for children, it can't get down to here without
    # having children

    # Look for solutions in each branch
    for child in temp_children:
        # This will return the first leaf that is not None
        # (so it's a solution) and exit the loop
        if str(child) not in seen:
            new_puzzle_node.children.append(PuzzleNode(child,
                                                   child.extensions(),
                                                   new_puzzle_node))

        new_depth = depth_helper(child, seen, stop_it)

        if new_depth is not None \
                and str(child) not in seen:
            return new_depth


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
    new_puzzle_node = PuzzleNode(puzzle)
    to_check = deque()
    to_check.append(new_puzzle_node)
    seen = []

    while to_check:
        puzzle_node = to_check.popleft()
        if puzzle_node.puzzle.fail_fast():
            return None
        if puzzle_node not in seen:
            # Check if the puzzle configuration is a solution
            # and return it straight away if it is
            if puzzle_node.puzzle.is_solved():
                return puzzle_node

            if puzzle_node.puzzle.extensions():
                # If there are extensions add children all at once to the queue
                for extension in puzzle_node.puzzle.extensions():
                    new_node = PuzzleNode(extension, None, puzzle_node)
                    to_check.append(new_node)
            seen.append(puzzle_node)

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
        True
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
