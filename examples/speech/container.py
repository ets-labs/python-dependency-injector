"""IoC container example."""

import collections

import dependency_injector.containers as containers
import dependency_injector.providers as providers


Engine = collections.namedtuple('Engine', [])
Car = collections.namedtuple('Car', ['serial_number', 'engine'])


class Container(containers.DeclarativeContainer):
    """IoC container."""

    engine_factory = providers.Factory(Engine)

    car_factory = providers.Factory(Car, engine=engine_factory)


if __name__ == '__main__':
    car1 = Container.car_factory(serial_number=1)
    car2 = Container.car_factory(serial_number=2)

    assert car1.serial_number == 1 and car2.serial_number == 2
    assert car1.engine is not car2.engine
