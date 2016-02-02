from unittest import TestCase

from othello.game import *


class OthelloTest(TestCase):

    def test_on_board_true(self):
        board = Board()
        self.assertTrue(board.on_board(board.parse_index('a5')))
        self.assertTrue(board.on_board(board.parse_index('g8')))
        self.assertTrue(board.on_board(board.parse_index('h8')))
        self.assertFalse(board.on_board(board.parse_index('i5')))
    
    def test_on_board_with_false(self):
        board = Board()
        # might be that this should actually return false?
        for test in ('xy', '-1g', '98', 'gg', 'qu', '11a', 'a11'):
            print(board.parse_index(test))
            self.assertFalse(board.on_board(board.parse_index(test)))

    def test_is_legal_move(self):
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
        # NOTE: double check player indices
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
