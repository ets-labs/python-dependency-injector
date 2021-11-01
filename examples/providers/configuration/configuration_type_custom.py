"""`Configuration` provider custom type specification example."""

import os
import decimal

from dependency_injector import containers, providers


class Calculator:
    def __init__(self, pi: decimal.Decimal):
        self.pi = pi


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()

    calculator_factory = providers.Factory(
        Calculator,
        pi=config.pi.as_(decimal.Decimal),
    )


if __name__ == "__main__":
    container = Container()

    # Emulate environment variables
    os.environ["PI"] = "3.1415926535897932384626433832"

    container.config.pi.from_env("PI")

    calculator = container.calculator_factory()

    assert calculator.pi == decimal.Decimal("3.1415926535897932384626433832")
