"""Main module."""

import sys

from dependency_injector.wiring import Provide

from .dispatcher import Dispatcher
from .containers import Container


def main(dispatcher: Dispatcher = Provide[Container.dispatcher]) -> None:
    dispatcher.run()


if __name__ == '__main__':
    container = Container()
    container.config.from_yaml('config.yml')
    container.configure_logging()
    container.wire(modules=[sys.modules[__name__]])

    main()
