"""`FactoryAggregate` providers example."""

import sys

import dependency_injector.providers as providers

from games import Chess, Checkers, Ludo


game_factory = providers.FactoryAggregate(chess=providers.Factory(Chess),
                                          checkers=providers.Factory(Checkers),
                                          ludo=providers.Factory(Ludo))

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
