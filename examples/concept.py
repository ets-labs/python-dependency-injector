"""Concept example of objects catalogs."""


from objects import AbstractCatalog

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


class ObjectB(object):

    """Example class ObjectB, that has dependencies on ObjectA and database."""

    def __init__(self, a, db):
        """Initializer."""
        self.a = a
        self.db = db


class Catalog(AbstractCatalog):

    """Catalog of objects providers."""

    database = Singleton(sqlite3.Connection,
                         InitArg('database', ':memory:'),
                         Attribute('row_factory', sqlite3.Row))
    """:type: (objects.Provider) -> sqlite3.Connection"""

    object_a = NewInstance(ObjectA,
                           InitArg('db', database))
    """:type: (objects.Provider) -> ObjectA"""

    object_b = NewInstance(ObjectB,
                           InitArg('a', object_a),
                           InitArg('db', database))
    """:type: (objects.Provider) -> ObjectB"""


# Catalog static provides.
a1, a2 = Catalog.object_a(), Catalog.object_a()
b1, b2 = Catalog.object_b(), Catalog.object_b()

# Some asserts.
assert a1 is not a2
assert b1 is not b2
assert a1.db is a2.db is b1.db is b2.db is Catalog.database()


# Dependencies injection (The Python Way) into class.
class Consumer(object):

    """Example consumer class."""

    dependencies = Catalog(Catalog.object_a,
                           Catalog.object_b)

    def example(self):
        """Example method."""
        a1 = self.dependencies.object_a()
        a2 = self.dependencies.object_a()

        b1 = self.dependencies.object_b()
        b2 = self.dependencies.object_b()

        # Some asserts.
        assert a1 is not a2
        assert b1 is not b2
        assert a1.db is a2.db is b1.db is b2.db

        try:
            self.dependencies.database()
        except AttributeError:
            pass
        else:
            raise Exception('Database is not listed as a dependency')


Consumer().example()


# Dependencies injection (The Python Way) into a callback.
def consumer_callback(dependencies=Catalog(Catalog.object_a,
                                           Catalog.object_b)):
    """Example function."""
    a1 = dependencies.object_a()
    a2 = dependencies.object_a()

    b1 = dependencies.object_b()
    b2 = dependencies.object_b()

    # Some asserts.
    assert a1 is not a2
    assert b1 is not b2
    assert a1.db is a2.db is b1.db is b2.db

    try:
        dependencies.database()
    except AttributeError:
        pass
    else:
        raise Exception('Database is not listed as a dependency')
