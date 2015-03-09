"""Config provider examples."""

from objects import AbstractCatalog

from objects.providers import Config
from objects.providers import NewInstance

from objects.injections import InitArg


class ObjectA(object):

    """Example class ObjectA, that has dependencies on some setting values."""

    def __init__(self, fee, price, timezone):
        """Initializer."""
        self.fee = fee
        self.price = price
        self.timezone = timezone


class Catalog(AbstractCatalog):

    """Catalog of objects providers."""

    config = Config()
    """:type: (objects.Config)"""

    object_a = NewInstance(ObjectA,
                           InitArg('fee', config.FEE),
                           InitArg('price', config.PRICE),
                           InitArg('timezone', config.GLOBAL.TIMEZONE))
    """:type: (objects.Provider) -> ObjectA"""


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
