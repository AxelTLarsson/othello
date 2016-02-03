from othello.game import *


def play():
    """Entry point for the application script"""
    board = Board()
    players = [Player('black'), Player('white')]
    game = Game(board, players)
    game.play()

if __name__ == '__main__':
    play()
