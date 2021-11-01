"""Main module."""

from dependency_injector.wiring import inject, Provide

from .dispatcher import Dispatcher
from .containers import Container


@inject
def main(dispatcher: Dispatcher = Provide[Container.dispatcher]) -> None:
    dispatcher.run()


if __name__ == "__main__":
    container = Container()
    container.init_resources()
    container.wire(modules=[__name__])

    main()
