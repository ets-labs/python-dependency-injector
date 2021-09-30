"""`Dict` provider example."""

import dataclasses
from typing import Dict

from dependency_injector import containers, providers


@dataclasses.dataclass
class Module:
    name: str


@dataclasses.dataclass
class Dispatcher:
    modules: Dict[str, Module]


class Container(containers.DeclarativeContainer):

    dispatcher_factory = providers.Factory(
        Dispatcher,
        modules=providers.Dict(
            module1=providers.Factory(Module, name="m1"),
            module2=providers.Factory(Module, name="m2"),
        ),
    )


if __name__ == "__main__":
    container = Container()

    dispatcher = container.dispatcher_factory()

    assert isinstance(dispatcher.modules, dict)
    assert dispatcher.modules["module1"].name == "m1"
    assert dispatcher.modules["module2"].name == "m2"

    # Call "dispatcher = container.dispatcher_factory()" is equivalent to:
    # dispatcher = Dispatcher(
    #     modules={
    #         "module1": Module(name="m1"),
    #         "module2": Module(name="m2"),
    #     },
    # )
