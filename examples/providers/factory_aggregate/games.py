"""Example module."""


class Game(object):
    """Base game class."""

    def play(self):
        """Play game."""
        print('Playing {0}'.format(self.__class__.__name__.lower()))


class Chess(Game):
    """Chess game."""


class Checkers(Game):
    """Checkers game."""


class Ludo(Game):
    """Ludo game."""
