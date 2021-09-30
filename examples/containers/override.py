"""Container overriding example."""

from dependency_injector import containers, providers


class Service:
    ...


class ServiceStub:
    ...


class Container(containers.DeclarativeContainer):

    service = providers.Factory(Service)


class OverridingContainer(containers.DeclarativeContainer):

    service = providers.Factory(ServiceStub)


if __name__ == "__main__":
    container = Container()
    overriding_container = OverridingContainer()

    container.override(overriding_container)

    service = container.service()
    assert isinstance(service, ServiceStub)
