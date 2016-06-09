"""Example of inversion of control container for Car & Engine example."""

import dependency_injector.containers as containers
import dependency_injector.providers as providers

import car_engine_ioc


class Container(containers.DeclarativeContainer):
    """IoC container of component providers."""

    engine = providers.Factory(car_engine_ioc.Engine)

    car = providers.Factory(car_engine_ioc.Car,
                            engine=engine)


if __name__ == '__main__':
    car = Container.car()  # Application creates Car's instance
