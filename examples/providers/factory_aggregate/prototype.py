"""FactoryAggregate provider prototype."""


class FactoryAggregate(object):
    """FactoryAggregate provider prototype."""

    def __init__(self, **factories):
        """Initializer."""
        self.factories = factories

    def __call__(self, factory_name, *args, **kwargs):
        """Create object."""
        return self.factories[factory_name](*args, **kwargs)

    def __getattr__(self, factory_name):
        """Return factory with specified name."""
        return self.factories[factory_name]
