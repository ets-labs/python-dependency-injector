"""Catalog overriding example."""

import sqlite3

from objects.catalog import AbstractCatalog
from objects.catalog import override

from objects.providers import Singleton
from objects.providers import NewInstance

from objects.injections import KwArg
from objects.injections import Attribute


class ObjectA(object):

    """ObjectA has dependency on database."""

    def __init__(self, database):
        """Initializer.

        Database dependency need to be injected via init arg."""
        self.database = database

    def get_one(self):
        """Select one from database and return it."""
        return self.database.execute('SELECT 1')


class ObjectAMock(ObjectA):

    """Mock of ObjectA.

    Has no dependency on database.
    """

    def __init__(self):
        """Initializer."""

    def get_one(self):
        """Select one from database and return it.

        Mock makes no database queries and always returns two instead of one.
        """
        return 2


class Catalog(AbstractCatalog):

    """Catalog of objects providers."""

    database = Singleton(sqlite3.Connection,
                         KwArg('database', ':memory:'),
                         KwArg('timeout', 30),
                         KwArg('detect_types', True),
                         KwArg('isolation_level', 'EXCLUSIVE'),
                         Attribute('row_factory', sqlite3.Row))

    object_a = NewInstance(ObjectA,
                           KwArg('database', database))


@override(Catalog)
class SandboxCatalog(Catalog):

    """Sandbox objects catalog with some mocks that overrides Catalog."""

    object_a = NewInstance(ObjectAMock)


# Creating several `ObjectA` instances.
object_a_1 = Catalog.object_a()
object_a_2 = Catalog.object_a()

# Making some asserts.
assert object_a_1 is not object_a_2
assert object_a_1.get_one() == object_a_2.get_one() == 2
