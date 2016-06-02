"""Factory provider keyword argument injections example."""

import collections

import dependency_injector.providers as providers


Engine = collections.namedtuple('Engine', [])
Car = collections.namedtuple('Car', ['serial_number', 'engine'])

engine_factory = providers.Factory(Engine)
car_factory = providers.Factory(Car, engine=engine_factory)


if __name__ == '__main__':
    car1 = car_factory(serial_number=1)
    car2 = car_factory(serial_number=2)

    assert car1.serial_number == 1 and car2.serial_number == 2
    assert car1.engine is not car2.engine
