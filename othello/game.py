import numpy as np
import re
import argparse
import os
from othello.players import Human, MiniMaxAI, AlphaBetaAI


class Board:
    """
    Represents the board as an 8 x 8 matrix, where 0:s are unoccupied tiles,
    and players' tiles are given by their numeric representation from int()
    in the Player class.
    """

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
        Return true if position is on the board.
        """
        if position is None:
            # self.parse_index will return None for an invalid input
            return False

        for p in position:
            if p < 0 or p > 7:
                return False
        else:
            return True

    # def __getattr__(self, *args, **kwargs):
    #     return self._board.__getattribute__(*args, **kwargs)

    def parse_index(self, item):
        """
        Convert alphanumeric index into numeric form.
        E.g. parse_index('2c') == parse_index('c2') == (1, 2)
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

    def parse_numeric_index(self, item):
        """
        Convert numeric index into human-readable alphanumeric form.
        E.g. parse_numeric_index((1, 2)) == 'c2'
        """
        # IMPORTANT: Board[n1, n2] is interpreted as 'n1 deciding the vertical
        # position (i.e. [0, 7]), 'n2' the horizontal position (i.e. [a,h])
        # In the code n1 is referred to as x and n2 as y!
        x, y = item
        return Board.order[y] + str(x + 1)

    def any(self, *args, **kwargs):
        return self._board.any(*args, **kwargs)

    def sum(self, *args, **kwargs):
        return self._board.sum(*args, **kwargs)

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

    def __mul__(self, other):
        return np.multiply(self._board, other)

    def __rmul__(self, other):
        return np.multiply(other, self._board)


class Game:
    """
    Handles the actual game play, defining allowable moves, starting positions.
    """

    def __init__(self, board, players, visualise=False):
        self.players = players
        self.board = board
        self.visualise = visualise
        self.current_player = players[0]
        self.other_player = players[1]

        # set the starting positions of the players
        self.board['4d'] = int(players[1])
        self.board['4e'] = int(players[0])
        self.board['5d'] = int(players[0])
        self.board['5e'] = int(players[1])

    def swap_players(self):
        self.other_player, self.current_player = \
            self.current_player, self.other_player

    def get_valid_flips(self, place):
        """
        For a suggested move, given by 'place', return the tiles to be flipped,
        if any, otherwise return None.
        """
        if place is None:
            return None

        # check that the tile is not taken
        if self.board[place] != 0:
            return None

        # check that the position is within the board
        if not self.board.on_board(place):
            return None

        tiles_to_flip = list()
        # go through possible directions, i.e. [0,1] is tile above,
        for xdir, ydir in ([0, 1], [1, 1], [1, 0], [1, -1], [0, -1],
                           [-1, -1], [-1, 0], [-1, 1]):
            x, y = place  # x-y position
            x += xdir
            y += ydir

            # check next direction if current one is not within board
            if not self.board.on_board((x, y)):
                continue

            # go as far as possible in current direction
            # while tiles are of opposing colour
            while self.board[x, y] == int(self.other_player):
                x += xdir
                y += ydir
                if not self.board.on_board((x, y)):
                    break

            # again, test another direction if not on board
            # (opposing player's tiles are stretched all the way to an edge)
            if not self.board.on_board((x, y)):
                continue

            # if current stretch is "anchored" by this player's tile, we're ok
            if self.board[x, y] == int(self.current_player):
                # build a list of all the tiles to flip
                while True:
                    x -= xdir
                    y -= ydir
                    if (x, y) == place:
                        break
                    tiles_to_flip.append((x, y))

        return tiles_to_flip if tiles_to_flip else None

    def get_tiles_to_flip(self, place):
        return self.get_valid_flips(place)

    def flip_tiles(self, tiles):
        """
        Flip all tiles in 'tiles' to the colour of 'player'.
        """
        for tile in tiles:
            self.board[tile] = int(self.current_player)

    def legal_moves(self):
        """
        Return a list of all possible legal moves on the board for 'player'.
        """
        legal_moves = list()
        for x in range(8):
            for y in range(8):
                flips = self.get_valid_flips((x, y))
                if flips:
                    legal_moves.append((x, y))
        return legal_moves

    def clear(self):
        """
        Clear terminal window.
        """
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_help(self):
        """
        Print friendly help text of how to play.
        """
        print('Make a move by specifying coordinates, such as "a1" or "1a".')
        print('Show this help text by typing "h" or "help".')
        print('Exit the game at any time by typing "q" or "quit".')

    def move(self, place, flips=None):
        if not flips:
            self.flip_tiles(self.get_valid_flips(place))
        else:
            self.flip_tiles(flips)
        self.board[place] = int(self.current_player)

    def is_terminal(self):
        """
        Just a very basic test at the moment checks if there are any zeros.
        :return:
        """
        return not self.board.any()

    def play(self):
        """
        Start the game, alternating between players' turns.
        """
        finished = False
        position = None

        while not finished:
            if self.visualise:
                self.clear()
                if position is not None:
                    print("Player %s moved on %s" %
                          (str(self.other_player),
                           self.board.parse_numeric_index(position)))
                print(self.board)
            else:
                # todo: print output move from AI
                pass

            # Check that moves are actually available for current player
            if self.legal_moves() == []:
                self.swap_players()
                if self.legal_moves() == []:
                    # Game over
                    print('No legal moves available for any player!')
                    break
                else:
                    print('No legal moves available for player %s!' %
                          self.other_player)
                    # other player's turn instead, we just pass because we've
                    # already swapped

            # loop until we get some valid input
            while True:
                position = self.current_player.get_move(self)

                if isinstance(self.current_player, Human):
                    if position.upper() == 'Q' or position.upper() == 'QUIT':
                        return
                    elif position.upper() == 'H' or position.upper() == 'HELP':
                        self.print_help()
                        continue

                    position = self.board.parse_index(position)

                tiles = self.get_valid_flips(position)
                if tiles:
                    self.move(position, tiles)
                    break
                else:
                    print('Illegal move!')
                    # we do not update i here, since 'player' is not updated
                    # in this loop anyway

            self.swap_players()

        # game finished
        player_tiles = self.nbr_of_tiles(self.current_player)
        other_tiles = self.nbr_of_tiles(self.other_player)
        if player_tiles > other_tiles:
            print("Player {} won with {} tiles over player {}'s {} tiles!"
                  .format(self.current_player, player_tiles, self.other_player,
                          other_tiles))
        elif other_tiles > player_tiles:
            print("Player {} won with {} tiles over player {}'s {} tiles!"
                  .format(self.other_player, other_tiles, self.current_player,
                          player_tiles))
        else:
            print("It's a draw!'")

    def nbr_of_tiles(self, player):
        """
        Get the number of tiles on the board belonging to 'player'.
        """
        nbr = 0
        for x in np.nditer(self.board._board):
            if x == int(player):
                nbr += 1
        return nbr

    def __mul__(self, other):
        return self.board * other

    def __rmul__(self, other):
        return other * self.board


def main():
    parser = argparse.ArgumentParser(description='Play othello vs an AI.')
    parser.add_argument(
        '-v', '--visualise',
        help='visualise game board, default is to output only AI moves',
        action='store_true')
    parser.add_argument(
        '-t', '--time',
        type=int,
        help='time limit in seconds for each ply, default is 10s',
        default=10)
    args = parser.parse_args()
    board = Board()
    # players = [Human('black'), Human('white')]
    players = [Human('black'), MiniMaxAI('white')]

    game = Game(board, players, args.visualise)
    game.play()


if __name__ == '__main__':
    main()
