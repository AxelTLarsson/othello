from collections import OrderedDict
from copy import deepcopy
from unittest import TestCase

from othello.players import MiniMaxAI, AlphaBetaAI


class TestGame:
    """
    A test game mirroring the example in the book to test the AI.
    """
    def __init__(self):
        self.state = 'start'

        self.scores = {
            'a1': 10, 'a2': 15, 'a3': 4,
            'b1':  3, 'b2': 12, 'b3': 8,
            'c1':  2, 'c2':  4, 'c3': 6,
            'd1': 14, 'd2':  5, 'd3': 2,
        }

        self.states = OrderedDict([
            ('a1', OrderedDict([('b1', 'x'), ('b2', 'x'), ('b3', 'x')])),
            ('a2', OrderedDict([('c1', 'x'), ('c2', 'x'), ('c3', 'x')])),
            ('a3', OrderedDict([('d1', 'x'), ('d2', 'x'), ('d3', 'x')])),
        ])

    @property
    def board(self):
        return self.scores[self.state]

    def move(self, place):
        assert place in self.states.keys()
        self.state = place
        self.states = self.states[place]

    def legal_moves(self):
        try:
            return list(self.states.keys())
        except AttributeError:
            return None

    def is_terminal(self):
        return self.states is 'x'

    def copy(self):
        return deepcopy(self)

    def __mul__(self, other):
        return self.scores[self.state] * other

    def __rmul__(self, other):
        return self.scores[self.state] * other


class MiniMaxAITest(TestCase):

    def test_basic_minimax(self):
        ai = MiniMaxAI(1, time_limit=10)
        game = TestGame()
        self.assertEqual('a1', ai.search(game))

    def test_depth_limited_search(self):
        ai = MiniMaxAI(1, time_limit=10, depth=0)
        game = TestGame()
        self.assertEqual('a2', ai.search(game))


class AlphaBetaAITest(TestCase):
    def test_basic_alpha_beta(self):
        ai = AlphaBetaAI(1, time_limit=10)
        game = TestGame()
        self.assertEqual('a1', ai.search(game))
