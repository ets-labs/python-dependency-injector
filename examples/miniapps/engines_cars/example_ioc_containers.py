"""Dependency injection example, Cars & Engines IoC containers."""

import example.cars
import example.engines

import dependency_injector.containers as containers
import dependency_injector.providers as providers


class Engines(containers.DeclarativeContainer):
    """IoC container of engine providers."""

    gasoline = providers.Factory(example.engines.GasolineEngine)

    diesel = providers.Factory(example.engines.DieselEngine)

    electric = providers.Factory(example.engines.ElectricEngine)


class Cars(containers.DeclarativeContainer):
    """IoC container of car providers."""

    gasoline = providers.Factory(example.cars.Car,
                                 engine=Engines.gasoline)

    diesel = providers.Factory(example.cars.Car,
                               engine=Engines.diesel)

    electric = providers.Factory(example.cars.Car,
                                 engine=Engines.electric)


if __name__ == '__main__':
    gasoline_car = Cars.gasoline()
    diesel_car = Cars.diesel()
    electric_car = Cars.electric()
