"""`Configuration` provider values loading example."""

from datetime import date

from dependency_injector import containers, providers


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()


if __name__ == "__main__":
    container = Container()

    container.config.option1.from_value(date(2022, 3, 13))
    container.config.option2.from_value(date(2022, 3, 14))

    assert container.config() == {
        "option1": date(2022, 3, 13),
        "option2": date(2022, 3, 14),
    }
    assert container.config.option1() == date(2022, 3, 13)
    assert container.config.option2() == date(2022, 3, 14)
