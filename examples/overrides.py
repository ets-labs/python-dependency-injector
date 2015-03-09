"""Override example."""


from objects import AbstractCatalog
from objects import overrides

from objects.providers import Singleton
from objects.providers import NewInstance

from objects.injections import InitArg
from objects.injections import Attribute

import sqlite3


class ObjectA(object):

    """Example class ObjectA, that has dependency on database."""

    def __init__(self, db):
        """Initializer."""
        self.db = db


class ObjectAMock(ObjectA):

    """Mock of ObjectA example class."""


class Catalog(AbstractCatalog):

    """Catalog of objects providers."""

    database = Singleton(sqlite3.Connection,
                         InitArg('database', ':memory:'),
                         Attribute('row_factory', sqlite3.Row))
    """:type: (objects.Provider) -> sqlite3.Connection"""

    object_a = NewInstance(ObjectA,
                           InitArg('db', database))
    """:type: (objects.Provider) -> ObjectA"""


@overrides(Catalog)
class SandboxCatalog(Catalog):

    """Sandbox objects catalog with some mocks that overrides Catalog."""

    object_a = NewInstance(ObjectAMock,
                           InitArg('db', Catalog.database))
    """:type: (objects.Provider) -> ObjectA"""


# Catalog static provides.
a1 = Catalog.object_a()
a2 = Catalog.object_a()

# Some asserts.
assert isinstance(a1, ObjectAMock)
assert isinstance(a2, ObjectAMock)
assert a1 is not a2
assert a1.db is a2.db is Catalog.database()
