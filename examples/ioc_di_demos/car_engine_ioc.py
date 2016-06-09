"""Refactored Car & Engine example that demonstrates inversion of control."""


class Engine(object):
    """Example engine."""


class Car(object):
    """Example car."""

    def __init__(self, engine):
        """Initializer."""
        self.engine = engine  # Engine is an "injected" dependency


if __name__ == '__main__':
    engine = Engine()  # Application creates Engine's instance
    car = Car(engine)  # and inject it into the Car's instance
