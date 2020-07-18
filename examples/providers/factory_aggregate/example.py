"""`FactoryAggregate` providers example."""

import sys

import dependency_injector.providers as providers

from games import Chess, Checkers, Ludo


game_factory = providers.FactoryAggregate(
    chess=providers.Factory(Chess),
    checkers=providers.Factory(Checkers),
    ludo=providers.Factory(Ludo),
)

if __name__ == '__main__':
    game_type = sys.argv[1].lower()
    player1 = sys.argv[2].capitalize()
    player2 = sys.argv[3].capitalize()

    selected_game = game_factory(game_type, player1, player2)
    selected_game.play()

    # $ python example.py chess John Jane
    # John and Jane are playing chess
    #
    # $ python example.py checkers John Jane
    # John and Jane are playing checkers
    #
    # $ python example.py ludo John Jane
    # John and Jane are playing ludo
