from puzzle import Puzzle


class WordLadderPuzzle(Puzzle):
    """
    A word-ladder puzzle that may be solved, unsolved, or even unsolvable.
    """

    def __init__(self, from_word, to_word, ws):
        """
        Create a new word-ladder puzzle with the aim of stepping
        from from_word to to_word using words in ws, changing one
        character at each step.

        @type from_word: str
        @type to_word: str
        @type ws: set[str]
        @rtype: None
        """
        (self._from_word, self._to_word, self._word_set) = (from_word,
                                                            to_word, ws)
        # set of characters to use for 1-character changes
        self._chars = "abcdefghijklmnopqrstuvwxyz"

        # TODO
        # implement __eq__ and __str__
        # __repr__ is up to you

    def extensions(self):
        """
        Return list of extensions
        # override extensions
        # legal extensions are WordPadderPuzzles that have a from_word that can
        # be reached from this one by changing a single letter to one of those
        # in self._chars
        :type self: Puzzle
        :rtype: list[Puzzle]
        """
        # TODO

        good_words = []
        from_word, to_word, ws, chars = self._from_word, self._to_word, self.ws, self.chars

        if not self.is_solved():
            word_list = []

            for i in range(len(from_word)):
                word_list = [from_word[:i] + q + from_word[i + 1:] for q in chars]

            for word in word_list:
                # If the word is in the allowed words
                if word in ws:
                    good_words.append(word)
        return [WordLadderPuzzle(q, to_word, ws) for q in good_words]

    def is_solved(self):
            # TODO
        # override is_solved
        # this WordLadderPuzzle is solved when _from_word is the same as
        # _to_word
            return self._from_word == self._to_word

    def __eq__(self, other):
        return (type(other) == type(self) and
                self._from_word == other._from_word and
                self._to_word == other._to_word and
                self.chars == other.chars)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    from puzzle_tools import breadth_first_solve, depth_first_solve
    from time import time
    with open("words", "r") as words:
        word_set = set(words.read().split())
    w = WordLadderPuzzle("same", "cost", word_set)
    start = time()
    sol = breadth_first_solve(w)
    end = time()
    print("Solving word ladder from same->cost")
    print("...using breadth-first-search")
    print("Solutions: {} took {} seconds.".format(sol, end - start))
    start = time()
    sol = depth_first_solve(w)
    end = time()
    print("Solving word ladder from same->cost")
    print("...using depth-first-search")
    print("Solutions: {} took {} seconds.".format(sol, end - start))
