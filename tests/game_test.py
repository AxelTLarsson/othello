from unittest import TestCase

from othello.game import *


class GameTest(TestCase):

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

    def test_legal_moves_thoroughly(self):
        board = Board()
        white = Player('white')
        black = Player('black')
        game = Game(board, [black, white])
        # a specific instance that casued issues:
        """
            a   b   c   d   e   f   g   h
          +---+---+---+---+---+---+---+---+
        1 |   |   |   |   |   |   |   |   |
          +---+---+---+---+---+---+---+---+
        2 |   |   |   |   |   |   |   |   |
          +---+---+---+---+---+---+---+---+
        3 |   |   |   | * | * | * |   |   |
          +---+---+---+---+---+---+---+---+
        4 |   |   |   | * | * | * | O |   |
          +---+---+---+---+---+---+---+---+
        5 |   |   |   | * | * | * | O | * |
          +---+---+---+---+---+---+---+---+
        6 |   |   |   | * | * | * | O | * |
          +---+---+---+---+---+---+---+---+
        7 |   |   | * |   | * | * | O |   |
          +---+---+---+---+---+---+---+---+
        8 |   |   |   |   |   | O | O | O |
          +---+---+---+---+---+---+---+---+

        No legal moves available for player: black!

        """
        # the moves that led to the above situation, [black, white, ...]
        black_moves = ['d3', 'f5', 'f4', 'h5',
                       'g7', 'g8',  'f3', 'c7', 'h6', 'e7']
        white_moves = ['e3', 'e6', 'g5', 'f6',
                       'f7', 'd6', 'g6', 'f8', 'h8', 'g4']
        moves = list(zip(black_moves, white_moves))

        for move in moves:
            black_move, white_move = move

            # perform black move
            flips = game.get_valid_flips(
                black, white, board.parse_index(black_move))
            board[board.parse_index(black_move)] = int(black)
            game.flip_tiles(flips, black)

            # perform white move
            flips = game.get_valid_flips(
                white, black, board.parse_index(white_move))
            board[board.parse_index(white_move)] = int(white)
            game.flip_tiles(flips, white)

        # now check legal moves for black
        legal_moves = map(
            board.parse_numeric_index,
            game.legal_moves(black, white))
        self.assertEqual(
          sorted(['h3', 'h4', 'h7']), sorted(list(legal_moves)))

    def test_parsers(self):
        board = Board()
        self.assertEqual(board.parse_index('1a'), (0, 0))
        self.assertEqual(board.parse_index('h8'), (7, 7))
        self.assertEqual(board.parse_numeric_index((1, 1)), 'b2')
        self.assertEqual(board.parse_numeric_index((7, 7)), 'h8')
        self.assertEqual(board.parse_index('2b'),
                         board.parse_index(board.parse_numeric_index((1, 1))))

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
