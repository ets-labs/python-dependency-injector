"""`List` provider example."""

import dataclasses
from typing import List

from dependency_injector import containers, providers


@dataclasses.dataclass
class Module:
    name: str


@dataclasses.dataclass
class Dispatcher:
    modules: List[Module]


class Container(containers.DeclarativeContainer):

    dispatcher_factory = providers.Factory(
        Dispatcher,
        modules=providers.List(
            providers.Factory(Module, name="m1"),
            providers.Factory(Module, name="m2"),
        ),
    )


if __name__ == "__main__":
    container = Container()

    dispatcher = container.dispatcher_factory()

    assert isinstance(dispatcher.modules, list)
    assert dispatcher.modules[0].name == "m1"
    assert dispatcher.modules[1].name == "m2"

    # Call "dispatcher = container.dispatcher_factory()" is equivalent to:
    # dispatcher = Dispatcher(
    #     modules=[
    #         Module(name="m1"),
    #         Module(name="m2"),
    #     ],
    # )
