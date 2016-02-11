import unittest
import sys
import os.path

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from collections import OrderedDict
from copy import deepcopy
from unittest import TestCase
from othello.players import MiniMaxAI, AlphaBetaAI, Player
from othello.game import Board, Game


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
        # int of white player is 1
        ai = MiniMaxAI('white', time_limit=10)
        game = TestGame()
        self.assertEqual('a1', ai.search(game))

    def test_depth_limited_search(self):
        # int of white player is 1
        ai = MiniMaxAI('white', time_limit=10, depth=0)
        game = TestGame()
        self.assertEqual('a2', ai.search(game))

    def test_minimax_on_othello_3_0_optimum(self):
        board = Board()
        players = [Player('black'), Player('white')]
        game = Game(board, players, visualise=True)
        game.board[3, 2] = int(players[1])
        game.board[3, 1] = int(players[1])
        ai = MiniMaxAI(color='black', depth=0)
        self.assertEqual(ai.search(game), (3, 0))

    def test_minimax_on_othello_3_7_optimum(self):
        board = Board()
        players = [Player('black'), Player('white')]
        game = Game(board, players, visualise=True)
        game.board[3, 5] = int(players[0])
        game.board[3, 6] = int(players[0])
        game.swap_players()
        ai = MiniMaxAI(color='white', depth=0)
        self.assertEqual(ai.search(game), (3, 7))


# class AlphaBetaAITest(TestCase):
#     def test_basic_alpha_beta(self):
#         ai = AlphaBetaAI(1, time_limit=10)
#         game = TestGame()
#         self.assertEqual('a1', ai.search(game))

if __name__ == '__main__':
    unittest.main()

