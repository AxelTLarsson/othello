import numpy as np
import re


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
        """
        Returns true if position is on the board.
        """
        if position is None:
            # self.parse_index will return None for an invalid input
            return False

        for p in position:
            if p < 0 or p > 7:
                return False
        else:
            return True

    def __getattr__(self, *args, **kwargs):
        return self._board.__getattribute__(*args, **kwargs)

    def parse_index(self, item):
        """
        Convert alphanumeric index into numeric form.
        E.g. parse_index('1a') == (0, 0)
        """
        if re.match(r'\d[a-zA-Z]', item):
            pass  # number first, followed by letter
        elif re.match(r'[a-zA-Z]\d', item):
            item = item[::-1]  # letter first, followed by number (reverse it)
        else:
            return None  # not a valid combination of letter and number

        s1 = int(item[0]) - 1
        try:
            s2 = Board.order.index(item[1])
        except ValueError:
            return None
        return s1, s2

    def parse_numeric_index(self, x, y):
        """
        Convert numeric index into human-readable alphanumeric form.
        E.g. parse_numeric_index(0, 0) == '1a'
        """
        return Board.order[x] + str(y + 1)

    def __getitem__(self, item):
        if isinstance(item, str):
            return self._board[self.parse_index(item)]
        else:
            return self._board[item]

    def __setitem__(self, key, value):
        if isinstance(key, str):
            self._board[self.parse_index(key)] = value
        else:
            self._board[key] = value


class Game:
    def __init__(self, board, players):
        self.players = players
        self.board = board

        # set the starting positions of the players
        self.board['4d'] = int(players[1])
        self.board['4e'] = int(players[0])
        self.board['5d'] = int(players[0])
        self.board['5e'] = int(players[1])

    def move(self, color, place):
        assert color in (1, 2)
        assert 0 <= place[0] <= self.board.shape[0]
        assert 0 <= place[1] <= self.board.shape[1]
        assert self.get_valid_flips(color, place)

        self.board[place] = color
        # fill in all relevant squares

    def get_valid_flips(self, current_player, other_player, place):

        if place is None:
            return None  # place will be None if

        # check that the tile is not taken
        if self.board[place] != 0:
            return None

        # check that the position is within the board
        if not self.board.on_board(place):
            return None

        tiles_to_flip = list()
        for xdir, ydir in ([0, 1], [1, 1], [1, 0], [1, -1], [0, -1],
                           [-1, -1], [-1, 0], [-1, 1]):
            x, y = place  # x-y position
            x += xdir
            y += ydir
            if not self.board.on_board((x, y)):
                continue

            while self.board[x, y] == int(other_player):
                x += xdir
                y += ydir
                if not self.board.on_board((x, y)):
                    break

            if not self.board.on_board((x, y)):
                continue

            if self.board[x, y] == int(current_player):
                # build a list of all the tiles to flip
                while True:
                    x -= xdir
                    y -= ydir
                    if (x, y) == place:
                        break
                    tiles_to_flip.append((x, y))

        return tiles_to_flip if tiles_to_flip else None

    def flip_tiles(self, tiles, player):
        for tile in tiles:
            self.board[tile] = int(player)

    def legal_moves(self, player):
        # return a list of all legal moves on the board
        pass

    def play(self):
        finished = False

        i = 0

        while not finished:
            print(self.board)
            player = self.players[i % 2]
            other_player = self.players[(i + 1) % 2]

            # Check that moves are actually available for current player
            if self.legal_moves(player) == []:
                if self.legal_moves(other_player) == []:
                    # Game over
                    break
                else:
                    print('No legal moves available for player: %s!' % player)
                    i += 1  # other player's turn instead
                    continue

            prompt = 'Player %s: ' % player
            position = input(prompt)
            if position.upper() == 'Q':
                break

            position = self.board.parse_index(position)

            tiles = self.get_valid_flips(player, other_player, position)
            if tiles:
                self.board[position] = int(player)
                self.flip_tiles(tiles, player)
            else:
                print("Illegal move!")
                i -= 1

            i += 1
        else:
            # game finished
            print('Game over')
            pass


if __name__ == '__main__':
    board = Board()

    players = [Player('black'), Player('white')]

    game = Game(board, players)
    # board['5e'] = int(players[0])
    game.play()
