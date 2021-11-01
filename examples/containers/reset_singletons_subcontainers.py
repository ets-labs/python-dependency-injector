"""Container reset singletons in subcontainer example."""

from dependency_injector import containers, providers


class SubContainer(containers.DeclarativeContainer):

    service = providers.Singleton(object)


class Container(containers.DeclarativeContainer):

    service = providers.Singleton(object)
    sub = providers.Container(SubContainer)


if __name__ == "__main__":
    container = Container()

    service1 = container.service()
    service2 = container.sub().service()

    container.reset_singletons()

    assert service1 is not container.service()
    assert service2 is not container.sub().service()
