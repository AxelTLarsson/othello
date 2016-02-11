# othello
An AI playing the game of Reversi with Othello rules

[The assignment](http://cs.lth.se/eda132-applied-artificial-intelligence/programming-assignments/search/)

    a   b   c   d   e   f   g   h
  +---+---+---+---+---+---+---+---+
1 |   |   |   |   |   |   |   |   |
  +---+---+---+---+---+---+---+---+
2 |   |   |   |   |   |   |   |   |
  +---+---+---+---+---+---+---+---+
3 |   |   |   |   |   |   |   |   |
  +---+---+---+---+---+---+---+---+
4 |   |   |   | O | * |   |   |   |
  +---+---+---+---+---+---+---+---+
5 |   |   |   | * | O |   |   |   |
  +---+---+---+---+---+---+---+---+
6 |   |   |   |   |   |   |   |   |
  +---+---+---+---+---+---+---+---+
7 |   |   |   |   |   |   |   |   |
  +---+---+---+---+---+---+---+---+
8 |   |   |   |   |   |   |   |   |
  +---+---+---+---+---+---+---+---+

## Installation
0. Clone the repository.
1. Create virtualenv in the cloned dir: `virtualenv othello` (make sure virtualenv is Python3)
2. Change into the virtualenv and activate it: `cd othello` and `source bin/activate`.
3. Install with pip: `pip install -e .`
4. Run with `play -h` to get a friendly help text.

## Documentation
Refer to [doc/report.pdf](./doc/report.pdf).
