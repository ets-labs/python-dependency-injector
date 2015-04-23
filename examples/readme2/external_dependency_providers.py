"""External dependency providers example."""

from objects.catalog import AbstractCatalog

from objects.providers import Singleton
from objects.providers import NewInstance
from objects.providers import ExternalDependency

from objects.injections import KwArg
from objects.injections import Attribute

import sqlite3


class ObjectA(object):

    """Example class ObjectA, that has dependency on database."""

    def __init__(self, db):
        """Initializer."""
        self.db = db


class ObjectB(object):

    """Example class ObjectB, that has dependencies on ObjectA and database."""

    def __init__(self, a, db):
        """Initializer."""
        self.a = a
        self.db = db


class Catalog(AbstractCatalog):

    """Catalog of objects providers."""

    database = ExternalDependency(instance_of=sqlite3.Connection)
    """:type: (objects.Provider) -> sqlite3.Connection"""

    object_a = NewInstance(ObjectA,
                           KwArg('db', database))
    """:type: (objects.Provider) -> ObjectA"""

    object_b = NewInstance(ObjectB,
                           KwArg('a', object_a),
                           KwArg('db', database))
    """:type: (objects.Provider) -> ObjectB"""


# Satisfaction of external dependency.
Catalog.database.override(Singleton(sqlite3.Connection,
                                    KwArg('database', ':memory:'),
                                    Attribute('row_factory', sqlite3.Row)))

# Catalog static provides.
a1, a2 = Catalog.object_a(), Catalog.object_a()
b1, b2 = Catalog.object_b(), Catalog.object_b()

# Some asserts.
assert a1 is not a2
assert b1 is not b2
assert a1.db is a2.db is b1.db is b2.db is Catalog.database()
