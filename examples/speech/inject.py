"""@inject decorator example."""

from container import Container

from dependency_injector.injections import inject


@inject(car_factory=Container.car_factory.delegate())
@inject(extra_engine=Container.engine_factory)
def main(car_factory, extra_engine):
    """Run application."""
    car1 = car_factory(serial_number=1)
    car2 = car_factory(serial_number=2, engine=extra_engine)

    assert car1.serial_number == 1 and car2.serial_number == 2
    assert car1.engine is not car2.engine
    assert car2.engine is extra_engine


if __name__ == '__main__':
    main()
