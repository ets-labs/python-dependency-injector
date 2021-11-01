"""Container dependencies check example."""

from dependency_injector import containers, providers


class Container(containers.DeclarativeContainer):

    service1 = providers.Dependency()
    service2 = providers.Dependency()


if __name__ == "__main__":
    container = Container()
    container.check_dependencies()  # <-- raises error:
    # Container has undefined dependencies: "Container.service1", "Container.service2"
