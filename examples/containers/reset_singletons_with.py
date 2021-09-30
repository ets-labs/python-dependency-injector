"""Container reset singletons context manager example."""

from dependency_injector import containers, providers


class Container(containers.DeclarativeContainer):

    service = providers.Singleton(object)


if __name__ == "__main__":
    container = Container()

    service1 = container.service()

    with container.reset_singletons():
        service2 = container.service()

    service3 = container.service()

    assert service1 is not service2
    assert service2 is not service3
    assert service3 is not service1
