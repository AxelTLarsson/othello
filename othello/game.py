import numpy as np


class Player:
    white = 1
    black = 2

    def __init__(self, color):
        self.color = color

    def __str__(self):
        return self.color

    def __int__(self):
        if self.color == 'white':
            return Player.white
        elif self.color == 'black':
            return Player.black
        else:
            raise ValueError


class Board:

    order = 'abcdefgh'

    def __init__(self, shape=(8, 8)):
        self._board = np.zeros(shape=shape)

    def __str__(self):
        s = '    ' + '   '.join(Board.order) + '\n'
        line = '  +' + '---+' * self._board.shape[1] + '\n'
        s += line
        for i in range(self._board.shape[0]):
            s += '%s |' % str(i + 1)
            for j in range(self._board.shape[1]):
                s += ' %s |' % ' O*'[int(self._board[i, j])]
            s += '\n' + line
        return s

    def on_board(self, position):
        x, y = self.parse_index(position)
        for p in (x, y):
            if p < 0 or p > 7:
                return False
        else:
            return True

    def __getattr__(self, *args, **kwargs):
        return self._board.__getattribute__(*args, **kwargs)

    def parse_index(self, item):
        if item[0].isalpha():
            item = item[::-1]

        s1 = int(item[0]) - 1
        try:
            s2 = Board.order.index(item[1])
        except ValueError:
            s2 = -1
        return s1, s2

    def parse_numeric_index(self, x, y):
        return Board.order[x] + str(y + 1)

    def __getitem__(self, item):
        return self._board[self.parse_index(item)]

    def __setitem__(self, key, value):
        self._board[self.parse_index(key)] = value


class Game:
    def __init__(self, board, players):
        self.players = players
        self.board = board
        self.board['4d'] = int(players[0])
        self.board['4e'] = int(players[1])
        self.board['5d'] = int(players[1])
        self.board['5e'] = int(players[0])

    def move(self, color, place):
        assert color in (1, 2)
        assert 0 <= place[0] <= self.board.shape[0]
        assert 0 <= place[1] <= self.board.shape[1]
        assert self.is_legal_move(color, place)

        self.board[place] = color
        # fill in all relevant squares

    def is_legal_move(self, current_player, other_player, place):

        # check that the tile is not taken
        if self.board[place] != 0:
            return False

        # check that the position is within the board
        if not self.board.on_board(place):
            return False

        for xdir, ydir in ([0, 1], [1, 1], [1, 0], [1, -1], [0, -1],
                           [-1, -1], [-1, 0], [-1, 1]):
            x, y = self.board.parse_index(place)  # x-y position
            x += xdir
            y += ydir
            pos = self.board.parse_numeric_index(x, y)
            if not self.board.on_board(pos):
                continue

            while self.board[pos] == int(other_player):
                x += xdir
                y += ydir
                pos = self.board.parse_numeric_index(x, y)
                if not self.board.on_board(pos):
                    break

    def legal_moves(self, color):
        # return a list of all legal moves on the board
        pass

    def play(self):
        finished = False

        i = 0

        while not finished:
            print(self.board)
            player = self.players[i % 2]
            prompt = 'Player %s: ' % player
            position = input(prompt)
            if position.upper() == 'Q':
                break

            if self.is_legal_move(player, position):
                self.board[position] = int(player)
            else:
                print("Illegal move!")
                i -= 1

            i += 1
        else:
            # game finished
            pass


if __name__ == '__main__':
    board = Board()

    place = '2a'
    board[place] = 1

    players = [Player('black'), Player('white')]
    game = Game(board, players)
    game.play()

    print(board.on_board('a5'))
    print(board.on_board('k5'))
    print(board.on_board('9a'))

