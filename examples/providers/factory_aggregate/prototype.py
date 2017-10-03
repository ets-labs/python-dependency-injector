"""FactoryAggregate provider prototype."""


class FactoryAggregate(object):
    """FactoryAggregate provider prototype."""

    def __init__(self, **factories):
        """Initializer."""
        self._factories = factories

    def __getattr__(self, factory_name):
        """Return factory."""
        if factory_name not in self._factories:
            raise AttributeError('There is no such factory')
        return self._factories[factory_name]

    def create(self, factory_name, *args, **kwargs):
        """Create object."""
        if factory_name not in self._factories:
            raise AttributeError('There is no such factory')

        factory = self._factories[factory_name]

        return factory(*args, **kwargs)
