"""@inject decorator example."""

from container import Container

from dependency_injector.injections import inject


@inject(car1=Container.car_factory)
@inject(car2=Container.car_factory)
def main(car1, car2):
    """Main function."""
    assert car1 is not car2
    assert car1.engine is not car2.engine

if __name__ == '__main__':
    main()
