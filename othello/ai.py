
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

        self._expanded_states = []

    def mini_max_decision(self, state):
        moves = state.legal_moves()
        scores = [self.min_value(self.result(state, a)) for a in moves]
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

    def result(self, state, a):
        state_copy = state.copy()
        state_copy.move(a)
        return state_copy

    def alpha_beta_pruning(self):
        pass

    def utility(self, state):
        # here we're using the weight board to gauge how well a player is doing
        return (self._weight_board * state).sum()

    def __str__(self):
        return "AI class with %s expanded states" % self._expanded_states


class TestGame:
    """
    A test game mirroring the example in the book to test the AI.
    """

    def __init__(self):
        self.state = 'start'
        self.states = {
            'a1': {'b1':  3, 'b2': 12, 'b3': 8},
            'a2': {'c1':  2, 'c2':  4, 'c3': 6},
            'a3': {'d1': 14, 'd2':  5, 'd3': 2},
        }
        self.end_states = []
        for s in self.states.values():
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
    players = [Player('black'), Player('white')]
    ai = AI(players[0], time_limit=10)
    game = TestGame()
    print(ai.mini_max_decision(game))
