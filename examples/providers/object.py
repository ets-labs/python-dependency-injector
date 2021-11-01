"""`Object` provider example."""

from dependency_injector import containers, providers


class Container(containers.DeclarativeContainer):

    object_provider = providers.Object(1)


if __name__ == "__main__":
    container = Container()

    assert container.object_provider() == 1
