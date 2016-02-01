from unittest import TestCase

from othello.game import *


class TestJoke(TestCase):
    def test_is_string(self):
        board = Board()
        self.assertTrue(True)

    def test_on_board(self):
        board = Board()
        self.assertTrue(board.on_board('a5'))
        self.assertFalse(board.on_board('i5'))
