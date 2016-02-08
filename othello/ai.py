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

        self._expanded_states = 0

    def result(self, state, a):
        self._expanded_states += 1
        state_copy = state.copy()
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

    def search(self, state, depth=None):
        moves = state.legal_moves()
        scores = [self.min_value(self.result(state, a)) for a in moves]
        print(max(scores))
        return moves[np.argmax(scores)]

    def max_value(self, state):
        if state.is_terminal():
            return self.utility(state)
        v = -np.inf
        for a in state.legal_moves():
            v = max(v, self.min_value(self.result(state, a)))
        return v

    def min_value(self, state):
        if state.is_terminal():
            return self.utility(state)
        v = np.inf
        for a in state.legal_moves():
            v = min(v, self.max_value(self.result(state, a)))
        return v


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


class TestGame:
    """
    A test game mirroring the example in the book to test the AI.
    """
    def __init__(self):
        self.state = 'start'
        self.end_states = []

        # dict version
        self.states = OrderedDict()
        states = {
            'a1': {'b1':  3, 'b2': 12, 'b3': 8},
            'a2': {'c1':  2, 'c2':  4, 'c3': 6},
            'a3': {'d1': 14, 'd2':  5, 'd3': 2},
        }

        for k1 in sorted(states.keys()):
            self.states[k1] = OrderedDict()
            for k, v in sorted(states[k1].items(), key=lambda x: x[0]):
                self.states[k1][k] = v

        for s in states.values():
            self.end_states.extend(list(s.keys()))

    def move(self, place):
        assert place in self.states.keys()
        self.state = place
        self.states = self.states[place]

    def legal_moves(self):
        try:
            return list(self.states.keys())
        except AttributeError:
            return None

    def is_terminal(self):
        if self.state in self.end_states:
            return True
        else:
            return False

    def copy(self):
        return deepcopy(self)

    def __mul__(self, other):
        return self.states * other

    def __rmul__(self, other):
        return self.states * other


if __name__ == '__main__':
    ai = MiniMaxAI(1, time_limit=10)
    game = TestGame()
    print(ai.search(game))
    print(ai)

    ai = AlphaBetaAI(1, time_limit=10)
    game = TestGame()
    print(ai.search(game))
    # with the default setup this should have expanded two less nodes
    # than the standard mini-max search
    print(ai)
