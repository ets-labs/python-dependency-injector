"""Concept example of `Dependency Injector`."""

from dependency_injector.catalog import AbstractCatalog

from dependency_injector.providers import Factory
from dependency_injector.providers import Singleton

from dependency_injector.injections import KwArg
from dependency_injector.injections import Attribute
from dependency_injector.injections import inject

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

    """Catalog of dependency_injector providers."""

    database = Singleton(sqlite3.Connection,
                         KwArg('database', ':memory:'),
                         Attribute('row_factory', sqlite3.Row))
    """:type: (dependency_injector.Provider) -> sqlite3.Connection"""

    object_a_factory = Factory(ObjectA,
                               KwArg('db', database))
    """:type: (dependency_injector.Provider) -> ObjectA"""

    object_b_factory = Factory(ObjectB,
                               KwArg('a', object_a_factory),
                               KwArg('db', database))
    """:type: (dependency_injector.Provider) -> ObjectB"""


# Catalog static provides.
a1, a2 = Catalog.object_a_factory(), Catalog.object_a_factory()
b1, b2 = Catalog.object_b_factory(), Catalog.object_b_factory()

assert a1 is not a2
assert b1 is not b2
assert a1.db is a2.db is b1.db is b2.db is Catalog.database()


# Example of inline injections.
@inject(KwArg('a', Catalog.object_a_factory))
@inject(KwArg('b', Catalog.object_b_factory))
@inject(KwArg('database', Catalog.database))
def example(a, b, database):
    """Example callback."""
    assert a.db is b.db is database is Catalog.database()


example()
