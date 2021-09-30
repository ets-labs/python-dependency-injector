"""Dynamic container example."""

from dependency_injector import containers, providers


if __name__ == "__main__":
    container = containers.DynamicContainer()
    container.factory1 = providers.Factory(object)
    container.factory2 = providers.Factory(object)

    object1 = container.factory1()
    object2 = container.factory2()

    print(container.providers)
    # {
    #     "factory1": <dependency_injector.providers.Factory(...),
    #     "factory2": <dependency_injector.providers.Factory(...),
    # }
