"""Overriding of factory provider example."""

import collections

import dependency_injector.providers as providers


Engine = collections.namedtuple('Engine', [])
Car = collections.namedtuple('Car', ['serial_number', 'engine'])

engine_factory = providers.Factory(Engine)
car_factory = providers.Factory(Car, engine=engine_factory)

EngineX = collections.namedtuple('EngineX', [])
engine_factory.override(providers.Factory(EngineX))


if __name__ == '__main__':
    car1 = car_factory(serial_number=1)
    car2 = car_factory(serial_number=2, engine=Engine())

    assert car1.serial_number == 1 and car2.serial_number == 2
    assert car1.engine.__class__ is EngineX
    assert car2.engine.__class__ is Engine
