"""`Configuration` provider dynamic item selector."""

import dataclasses

from dependency_injector import containers, providers


@dataclasses.dataclass
class Foo:
    option1: object
    option2: object


class Container(containers.DeclarativeContainer):

    config = providers.Configuration(default={
        "target": "A",
        "items": {
            "A": {
                "option1": 60,
                "option2": 80,
            },
            "B": {
                "option1": 10,
                "option2": 20,
            },
        },
    })

    foo_factory = providers.Factory(
        Foo,
        option1=config.items[config.target].option1,
        option2=config.items[config.target].option2,
    )


if __name__ == "__main__":
    container = Container()

    container.config.target.from_env("TARGET")
    foo = container.foo_factory()
    print(foo.option1, foo.option2)

    # $ TARGET=A python configuration_itemselector.py
    # 60 80
    # $ TARGET=B python configuration_itemselector.py
    # 10 20
