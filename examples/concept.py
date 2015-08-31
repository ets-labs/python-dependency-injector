"""Concept example of `Dependency Injector`."""

import sqlite3
import dependency_injector as di


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


class Catalog(di.AbstractCatalog):

    """Catalog of providers."""

    database = di.Singleton(sqlite3.Connection,
                            di.KwArg('database', ':memory:'),
                            di.Attribute('row_factory', sqlite3.Row))
    """:type: (di.Provider) -> sqlite3.Connection"""

    object_a_factory = di.Factory(ObjectA,
                                  di.KwArg('db', database))
    """:type: (di.Provider) -> ObjectA"""

    object_b_factory = di.Factory(ObjectB,
                                  di.KwArg('a', object_a_factory),
                                  di.KwArg('db', database))
    """:type: (di.Provider) -> ObjectB"""


# Catalog static provides.
a1, a2 = Catalog.object_a_factory(), Catalog.object_a_factory()
b1, b2 = Catalog.object_b_factory(), Catalog.object_b_factory()

assert a1 is not a2
assert b1 is not b2
assert a1.db is a2.db is b1.db is b2.db is Catalog.database()


# Example of inline injections.
@di.inject(a=Catalog.object_a_factory)
@di.inject(b=Catalog.object_b_factory)
@di.inject(database=Catalog.database)
def example(a, b, database):
    """Example callback."""
    assert a.db is b.db is database is Catalog.database()


example()
