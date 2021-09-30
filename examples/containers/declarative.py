"""Declarative container example."""

from dependency_injector import containers, providers


class Container(containers.DeclarativeContainer):

    factory1 = providers.Factory(object)

    factory2 = providers.Factory(object)


if __name__ == "__main__":
    container = Container()

    object1 = container.factory1()
    object2 = container.factory2()

    print(container.providers)
    # {
    #     "factory1": <dependency_injector.providers.Factory(...),
    #     "factory2": <dependency_injector.providers.Factory(...),
    # }
