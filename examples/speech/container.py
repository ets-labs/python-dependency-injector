"""IoC container example."""

import collections

import dependency_injector.containers as containers
import dependency_injector.providers as providers


class Container(containers.DeclarativeContainer):
    """IoC container."""

    engine_factory = providers.Factory(collections.namedtuple('Engine', []))
    car_factory = providers.Factory(collections.namedtuple('Car', ['engine']),
                                    engine=engine_factory)

if __name__ == '__main__':
    car1 = Container.car_factory()
    car2 = Container.car_factory()

    assert car1 is not car2
    assert car1.engine is not car2.engine
