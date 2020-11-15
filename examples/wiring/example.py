"""Wiring example."""

import sys

from dependency_injector import containers, providers
from dependency_injector.wiring import inject, Provide


class Service:
    ...


class Container(containers.DeclarativeContainer):

    service = providers.Factory(Service)


@inject
def main(service: Service = Provide[Container.service]) -> None:
    ...


if __name__ == '__main__':
    container = Container()
    container.wire(modules=[sys.modules[__name__]])

    main()
