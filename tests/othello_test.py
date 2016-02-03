from unittest import TestCase

from othello.game import *


class OthelloTest(TestCase):

    def test_on_board(self):
        board = Board()

        # valid indices
        for test in ('a5', 'g8', 'h8', 'a1', '7c'):
            self.assertTrue(board.on_board(board.parse_index(test)))

        # invalid indices
        for test in ('xy', '-1g', '98', 'gg', 'qu', '11a', 'a11', 'i5'):
            self.assertFalse(board.on_board(board.parse_index(test)))

    def test_get_valid_flips(self):
        board = Board()
        players = [Player('black'), Player('white')]
        game = Game(board, players)

        player = game.players[0]
        other_player = game.players[1]

        # illegal moves should return false
        self.assertIsNone(game.get_valid_flips(player, other_player,
                                               board.parse_index('3l')))
        self.assertIsNone(game.get_valid_flips(player, other_player,
                                               board.parse_index('4d')))

        # all possible legal moves for starting black
        self.assertEqual(game.get_valid_flips(player, other_player,
                                              board.parse_index('3d')),
                         [board.parse_index('4d')])
        self.assertEqual(game.get_valid_flips(player, other_player,
                                              board.parse_index('4c')),
                         [board.parse_index('4d')])
        self.assertEqual(game.get_valid_flips(player, other_player,
                                              board.parse_index('6e')),
                         [board.parse_index('5e')])
        self.assertEqual(game.get_valid_flips(player, other_player,
                                              board.parse_index('5f')),
                         [board.parse_index('5e')])
