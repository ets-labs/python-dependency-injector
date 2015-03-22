"""Provider delegation example."""

from objects.catalog import AbstractCatalog

from objects.providers import Singleton
from objects.providers import NewInstance

from objects.injections import KwArg
from objects.injections import Attribute

import sqlite3


class ObjectA(object):

    """Example class ObjectA, that has dependency on database."""

    def __init__(self, db):
        """Initializer."""
        self.db = db


class ObjectB(object):

    """Example class ObjectB, that has dependency on ObjectA provider."""

    def __init__(self, a_provider):
        """Initializer."""
        self.a_provider = a_provider


class Catalog(AbstractCatalog):

    """Catalog of objects providers."""

    database = Singleton(sqlite3.Connection,
                         KwArg('database', ':memory:'),
                         Attribute('row_factory', sqlite3.Row))
    """:type: (objects.Provider) -> sqlite3.Connection"""

    object_a = NewInstance(ObjectA,
                           KwArg('db', database))
    """:type: (objects.Provider) -> ObjectA"""

    object_b = Singleton(ObjectB,
                         KwArg('a_provider', object_a.delegate()))
    """:type: (objects.Provider) -> ObjectB"""


# Catalog static provides.
b = Catalog.object_b()
a1, a2 = b.a_provider(), b.a_provider()

# Some asserts.
assert a1 is not a2
assert a1.db is a2.db is Catalog.database()
