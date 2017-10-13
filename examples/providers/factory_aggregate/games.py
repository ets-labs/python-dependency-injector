"""Example games module."""


class Game(object):
    """Base game class."""

    def __init__(self, player1, player2):
        """Initializer."""
        self.player1 = player1
        self.player2 = player2

    def play(self):
        """Play game."""
        print('{0} and {1} are playing {2}'.format(
            self.player1, self.player2, self.__class__.__name__.lower()))


class Chess(Game):
    """Chess game."""


class Checkers(Game):
    """Checkers game."""


class Ludo(Game):
    """Ludo game."""
