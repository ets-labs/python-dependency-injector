"""Config provider examples."""

from dependency_injector.catalog import AbstractCatalog
from dependency_injector.providers import Config
from dependency_injector.providers import Factory
from dependency_injector.injections import KwArg


class ObjectA(object):

    """Example class ObjectA, that has dependencies on some setting values."""

    def __init__(self, fee, price, timezone):
        """Initializer."""
        self.fee = fee
        self.price = price
        self.timezone = timezone


class Catalog(AbstractCatalog):

    """Catalog of dependency_injector providers."""

    config = Config()
    """:type: (dependency_injector.Config)"""

    object_a = Factory(ObjectA,
                       KwArg('fee', config.FEE),
                       KwArg('price', config.PRICE),
                       KwArg('timezone', config.GLOBAL.TIMEZONE))
    """:type: (dependency_injector.Provider) -> ObjectA"""


# Setting config value and making some tests.
Catalog.config.update_from({
    'FEE': 1.25,
    'PRICE': 2.99,
    'GLOBAL': {
        'TIMEZONE': 'US/Eastern'
    }
})

object_a1 = Catalog.object_a()

assert object_a1.fee == 1.25
assert object_a1.price == 2.99
assert object_a1.timezone == 'US/Eastern'

# Changing config value one more time and making some tests.
Catalog.config.update_from({
    'FEE': 5.25,
    'PRICE': 19.99,
    'GLOBAL': {
        'TIMEZONE': 'US/Western'
    }
})

object_a2 = Catalog.object_a()

# New one ObjectA has new config values.
assert object_a2.fee == 5.25
assert object_a2.price == 19.99
assert object_a2.timezone == 'US/Western'

# And old one has old ones.
assert object_a1.fee == 1.25
assert object_a1.price == 2.99
assert object_a1.timezone == 'US/Eastern'
