"""Car & Engine example 2."""


class Engine(object):
    """Example engine."""


class Car(object):
    """Example car."""

    def __init__(self, engine):
        """Initializer."""
        self.engine = engine


if __name__ == '__main__':
    car = Car(Engine())
    assert car.engine is not None
