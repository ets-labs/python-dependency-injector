"""`FactoryAggregate` providers example."""

import sys

from dependency_injector.providers import Factory

from prototype import FactoryAggregate
from games import Chess, Checkers, Ludo


game_factory = FactoryAggregate(chess=Factory(Chess),
                                checkers=Factory(Checkers),
                                ludo=Factory(Ludo))

if __name__ == '__main__':
    game_type = sys.argv[1].lower()
    selected_game = game_factory.create(game_type)
    selected_game.play()

    # $ python example.py chess
    # Playing chess

    # $ python example.py checkers
    # Playing checkers

    # $ python example.py ludo
    # Playing ludo
