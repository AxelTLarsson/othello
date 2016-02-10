from collections import OrderedDict

import numpy as np
from othello.game import Board, Player, Game
from copy import deepcopy


class WeightBoard(Board):
    def __str__(self):
        return str(self._board)

    def __add__(self, other):
        return self._board + other

    def __getattr__(self, *args, **kwargs):
        return self._board.__getattribute__(*args, **kwargs)


class AI:
    """
    Base class for MiniMax and AlphaBeta AI agents.
    """
    def __init__(self, player, time_limit=None, edge_weight=3, corner_weight=10,
                 depth=None):
        if depth is None:
            self.depth = np.inf
        else:
            self.depth = depth

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

        self._expanded_states = 0

    def result(self, state, a):
        self._expanded_states += 1

        state_copy = deepcopy(state)

        if state.__class__.__name__.startswith('Game'):
            # todo: need a way to copy this properly! (or don't copy at all??)
            state_copy.board = Board()
            state_copy.board._board = state.board._board.copy()

        print("Move: %s" % str(a))
        print("Flips: %s" % str(state_copy.get_tiles_to_flip(a)))
        state_copy.move(a)
        return state_copy

    def utility(self, state):
        """
        Here we use the weight board to gauge how well a player is doing

        :param state: Game, a game state
        :return: float/int, score for the current state given the player set
            at initialization
        """
        return (self._weight_board * state).sum() * int(self.player)

    def __str__(self):
        return ("%s for player %s: %s expanded states" %
                (self.__class__.__name__, self.player, self._expanded_states))


class MiniMaxAI(AI):

    def search(self, state):
        moves = state.legal_moves()
        scores = [self.min_value(self.result(state, a), self.depth)
                  for a in moves]
        print(max(scores))
        return moves[np.argmax(scores)]

    def max_value(self, state, depth):
        if self.cut_off(state, depth):
            return self.utility(state)
        v = -np.inf
        for a in state.legal_moves():
            v = max(v, self.min_value(self.result(state, a), depth-1))
        return v

    def min_value(self, state, depth):
        if self.cut_off(state, depth):
            return self.utility(state)
        v = np.inf
        for a in state.legal_moves():
            v = min(v, self.max_value(self.result(state, a), depth-1))
        return v

    def cut_off(self, state, depth):
        return state.is_terminal() or depth <= 0


class AlphaBetaAI(AI):

    def search(self, state):
        self.best_move = None
        v = self.max_value(state, -np.inf, np.inf)
        return v

    def max_value(self, state, alpha, beta):
        if state.is_terminal():
            return self.utility(state)
        v = -np.inf
        for a in state.legal_moves():
            v = max(v, self.min_value(self.result(state, a), alpha, beta))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(self, state, alpha, beta):
        if state.is_terminal():
            return self.utility(state)
        v = np.inf
        for a in state.legal_moves():
            v = min(v, self.max_value(self.result(state, a), alpha, beta))
            if v <= alpha:
                return v
            beta = min(alpha, v)
        return v


if __name__ == '__main__':
    board = Board()
    players = [Player('black'), Player('white')]
    game = Game(board, players, visualise=True)
    game.board[3, 2] = int(players[1])

    ai = MiniMaxAI(player=players[0], depth=0)
    print(ai.search(game))
