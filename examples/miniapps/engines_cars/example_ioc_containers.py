"""Dependency injection example, Cars & Engines IoC containers."""

import example.cars
import example.engines

import dependency_injector.containers as containers
import dependency_injector.providers as providers


class Engines(containers.DeclarativeContainer):
    """IoC container of engine providers."""

    gasoline = providers.Factory(example.engines.GasolineEngine)

    diesel = providers.Factory(example.engines.DieselEngine)

    electro = providers.Factory(example.engines.ElectroEngine)


class Cars(containers.DeclarativeContainer):
    """IoC container of car providers."""

    gasoline = providers.Factory(example.cars.Car,
                                 engine=Engines.gasoline)

    diesel = providers.Factory(example.cars.Car,
                               engine=Engines.diesel)

    electro = providers.Factory(example.cars.Car,
                                engine=Engines.electro)


if __name__ == '__main__':
    gasoline_car = Cars.gasoline()
    diesel_car = Cars.diesel()
    electro_car = Cars.electro()
