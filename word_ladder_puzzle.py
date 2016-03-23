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
    def __eq__(self, other):
        """
        Return true if WordLadderPuzzle object self equals other.

        :type self: WordLadderPuzzle
        :param other: WordLadderPuzzle
        :return: bool

        >>> from_word1 = 'cost'
        >>> to_word1 = 'save'
        >>> word_set1 = {'cast', 'case','cave','save'}
        >>> puzzle1 = WordLadderPuzzle(from_word1, to_word1, word_set1)
        >>> from_word2 = 'cost'
        >>> to_word2 = 'save'
        >>> word_set2 = {'cast', 'case','cave','save'}
        >>> puzzle2 = WordLadderPuzzle(from_word2, to_word2, word_set2)
        >>> puzzle1 == puzzle2
        True
        >>> from_word3 = 'carp'
        >>> to_word3 = 'save'
        >>> word_set3 = {'care', 'case','cave','save'}
        >>> puzzle3 = WordLadderPuzzle(from_word3, to_word3, word_set3)
        >>> puzzle1 == puzzle3
        False
        """

        return (type(other) == type(self) and
                self._from_word == other._from_word and
                self._to_word == other._to_word and
                self._word_set == other._word_set)

    def __str__(self):
        """
        :type self: WordLadderPuzzle
        rtype: Str
        >>> from_word = 'cast'
        >>> to_word = 'save'
        >>> word_set = {'cost', 'case','cave','save'}
        >>> puzzle = WordLadderPuzzle(from_word, to_word, word_set)
        >>> print(puzzle)
        cast --> save
        """

        return self._from_word + " --> " + self._to_word

    def __repr__(self):
        """
        Return a representation of WordLadderPuzzle self that can be evaluate to produce another WordLadderPuzzle.

        :type self: WordLadderPuzzle
        rtype: Str
        >>> from_word = 'cast'
        >>> to_word = 'save'
        >>> word_set = {'cost', 'case','cave','save'}
        >>> puzzle = WordLadderPuzzle(from_word, to_word, word_set)
        >>> puzzle.__repr__()
        "WordLadderPuzzle(cast, save, {'cost', 'case', 'cave', 'save'})"
        """

        # You may need to change str(self._word_set) to repr(self._word_set)
        result = "WordLadderPuzzle({}, {}, {})".format(self._from_word, self._to_word, self._word_set)
        return result

    def extensions(self):
        """
        Return list of legal WordLadderPuzzle extensions from self.
        # override extensions
        # legal extensions are WordPadderPuzzles that have a from_word that can
        # be reached from this one by changing a single letter to one of those
        # in self._chars
        :type self: WordLadderPuzzle
        :rtype: list[WordLadderPuzzle]

        >>> from_word = 'cast'
        >>> to_word = 'save'
        >>> word_set = {'cost', 'case','cave','save'}
        >>> puzzle = WordLadderPuzzle(from_word, to_word, word_set)
        >>> new_list = []
        >>> new_list.append(WordLadderPuzzle('cost', to_word, word_set))
        >>> new_list.append(WordLadderPuzzle('case', to_word, word_set))
        >>> new_list == puzzle.extensions()
        True
        """

        # TODO

        good_words = []
        from_word, to_word, ws, chars = self._from_word, self._to_word, self._word_set, self._chars

        if not self.is_solved():
            word_list = []

            for i in range(len(from_word)):
                for q in chars:
                    word_list.append(from_word[:i] + q + from_word[i + 1:])

            for word in word_list:
                if word in ws and (word not in good_words) and word != from_word:
                    good_words.append(word)
        return [WordLadderPuzzle(q, to_word, ws) for q in good_words]


    def is_solved(self):
            # TODO
        # override is_solved
        # this WordLadderPuzzle is solved when _from_word is the same as
        # _to_word
        """
        Return true if WordLadderPuzzle self is in a solved state.

        :type self: WordLadderPuzzle
        :rtype: bool

        >>> from_word = 'begin'
        >>> to_word = 'begin'
        >>> word_set = {'phone','brush','table'}
        >>> puzzle = WordLadderPuzzle(from_word, to_word, word_set)
        >>> puzzle.is_solved()
        True
        """

        return self._from_word == self._to_word


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
