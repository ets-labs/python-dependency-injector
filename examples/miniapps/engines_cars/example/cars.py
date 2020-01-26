"""Dependency injection example, cars module."""


class Car(object):
    """Example car."""

    def __init__(self, engine):
        """Initialize instance."""
        self._engine = engine  # Engine is injected
