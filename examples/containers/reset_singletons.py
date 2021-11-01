"""Container reset singletons example."""

from dependency_injector import containers, providers


class Container(containers.DeclarativeContainer):

    service1 = providers.Singleton(object)
    service2 = providers.Singleton(object)


if __name__ == "__main__":
    container = Container()

    service1 = container.service1()
    service2 = container.service2()

    container.reset_singletons()

    assert service1 is not container.service1()
    assert service2 is not container.service2()
