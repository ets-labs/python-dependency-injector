"""Config provider examples."""

import dependency_injector as di


class ObjectA(object):
    """Example class ObjectA, that has dependencies on some setting values."""

    def __init__(self, fee, price, timezone):
        """Initializer."""
        self.fee = fee
        self.price = price
        self.timezone = timezone


class Catalog(di.AbstractCatalog):
    """Catalog of providers."""

    config = di.Config()
    """:type: di.Config"""

    object_a = di.Factory(ObjectA,
                          fee=config.FEE,
                          price=config.PRICE,
                          timezone=config.GLOBAL.TIMEZONE)
    """:type: di.Provider -> ObjectA"""


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
