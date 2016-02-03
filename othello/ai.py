
from othello.game import Board, Player, Game


class WeightBoard(Board):
    def __str__(self):
        return str(self._board)

    def __add__(self, other):
        return self._board + other

    def __getattr__(self, *args, **kwargs):
        return self._board.__getattribute__(*args, **kwargs)


class AI:
    def __init__(self, player, time_limit, edge_weight=3, corner_weight=10):
        self.player = player
        self._time_limit = time_limit
        self._weight_board = WeightBoard() + 1

        # set the edges on the weight board
        self._weight_board[:, 0] = edge_weight
        self._weight_board[0, :] = edge_weight
        self._weight_board[:, -1] = edge_weight
        self._weight_board[-1, :] = edge_weight

        # set the corners to the corner weights
        self._weight_board[0, 0] = corner_weight
        self._weight_board[-1, 0] = corner_weight
        self._weight_board[0, -1] = corner_weight
        self._weight_board[-1, -1] = corner_weight

        print(self._weight_board)

    def find_best_move(self, game:Game, player):
        best_moves = dict()
        for move in game.legal_moves(player):
            

    def move_score(self, state, move):
        state[move] = int(self.player)
        return sum(self._weight_board * state)


if __name__ == '__main__':
    players = [Player('black'), Player('white')]
    ai = AI(players[0], time_limit=10)
