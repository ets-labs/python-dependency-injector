"""Car & Engine example 1."""


class Engine(object):
    """Example engine."""


class Car(object):
    """Example car."""

    def __init__(self):
        """Initializer."""
        self.engine = Engine()


if __name__ == '__main__':
    car = Car()
    assert car.engine is not None
