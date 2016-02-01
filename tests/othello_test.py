from unittest import TestCase

from othello.game import *


class OthelloTest(TestCase):

    def test_on_board(self):
        board = Board()
        self.assertTrue(board.on_board('a5'))
        self.assertTrue(board.on_board('g8'))
        self.assertTrue(board.on_board('h8'))
        self.assertFalse(board.on_board('i5'))
        
        # might be that this should actually return false?
        with self.assertRaises(ValueError):
            board.on_board('xy')
            board.on_board('-1g')
            board.on_board('98')
            board.on_board('gg')
            board.on_board('qu')

    def test_is_legal_move(self):
        board = Board()
        players = [Player('black'), Player('white')]
        game = Game(board, players)
        
        player = game.players[0]

        # illegal moves should return false
        self.assertFalse(game.is_legal_move(1, 2, '3l'))
        self.assertFalse(game.is_legal_move(1, 2, '4d'))

        # all possible legal moves for starting black
        # NOTE: double check player indices
        self.assertTrue(game.is_legal_move(1, 2, '3d'))
        self.assertTrue(game.is_legal_move(1, 2, '4c'))
        self.assertTrue(game.is_legal_move(1, 2, '6e'))
        self.assertTrue(game.is_legal_move(1, 2, '5g'))
