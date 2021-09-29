"""Wiring container injection example."""

from dependency_injector import containers, providers
from dependency_injector.wiring import Provide, inject


class Service:
    ...


class Container(containers.DeclarativeContainer):

    service = providers.Factory(Service)


@inject
def main(container: Container = Provide[Container]):
    service = container.service()
    ...


if __name__ == "__main__":
    container = Container()
    container.wire(modules=[__name__])

    main()
