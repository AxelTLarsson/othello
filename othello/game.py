import numpy as np


class Board:
    def __init__(self, shape=(8, 8)):
        self._board = np.zeros(shape=shape)

    def __str__(self):
        line = '+' + '---+' * self._board.shape[1] + '\n'
        s = line
        for i in range(self._board.shape[0]):
            s += '|'
            for j in range(self._board.shape[1]):
                s += ' %s |' % ' O*'[int(self._board[i, j])]
            s += '\n' + line
        return s

    def __getattr__(self, *args, **kwargs):
        return self._board.__getattribute__(*args, **kwargs)

    def __getitem__(self, item):
        return self._board[item]

    def __setitem__(self, key, value):
        assert 0 < value < 3
        self._board[key] = value


class Game:
    def __init__(self, board):
        self.board = board

    def move(self, color, place):
        assert color in (1, 2)
        assert 0 <= place[0] <= self.board.shape[0]
        assert 0 <= place[1] <= self.board.shape[1]
        assert self.is_legal_move(color, place)

        self.board[place] = color
        # fill in all relevant squares

    def is_legal_move(self, color, place):
        pass

    def legal_moves(self, color):
        # return a list of all legal moves on the board
        pass


if __name__ == '__main__':
    board = Board()

    board[4, 4] = 2
    board[4, 3] = 1
    board[4, 2] = 1

    place = (5, 5)
    board[place] = 1

    print(board)
    print(board.shape)
