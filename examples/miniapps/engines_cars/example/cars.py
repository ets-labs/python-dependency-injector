"""Dependency injection example, cars module."""


class Car(object):
    """Example car."""

    def __init__(self, engine):
        """Initializer."""
        self._engine = engine  # Engine is injected
