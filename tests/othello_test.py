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

    def test_legal_moves(self):
        board = Board()
        white = Player('white')
        black = Player('black')
        game = Game(board, [black, white])

        # test possible starting moves for black
        legal_moves = map(
            board.parse_numeric_index,
            game.legal_moves(black, white))
        self.assertEqual(['c4', 'd3', 'e6', 'f5'], list(legal_moves))

        # if white were to play first
        legal_moves = map(
            board.parse_numeric_index,
            game.legal_moves(white, black))
        self.assertEqual(
            sorted(['e3', 'f4', 'c5', 'd6']), sorted(list(legal_moves)))

        # assume black makes 'd3'
        flips = game.get_valid_flips(black, white, board.parse_index('d3'))
        board[board.parse_index('d3')] = int(black)
        game.flip_tiles(flips, black)

        # then check legal moves for white
        legal_moves = map(
            board.parse_numeric_index,
            game.legal_moves(white, black))
        self.assertEqual(
            sorted(['c3', 'e3', 'c5']), sorted(list(legal_moves)))

    def test_nbr_tiles(self):
        board = Board()
        white = Player('white')
        black = Player('black')
        game = Game(board, [black, white])
        self.assertEqual(game.nbr_of_tiles(black), 2)
        self.assertEqual(game.nbr_of_tiles(white), 2)
        # black makes move 'd3'
        flips = game.get_valid_flips(black, white, board.parse_index('d3'))
        board[board.parse_index('d3')] = int(black)
        game.flip_tiles(flips, black)

        self.assertEqual(game.nbr_of_tiles(white), 1)
        self.assertEqual(game.nbr_of_tiles(black), 4)
