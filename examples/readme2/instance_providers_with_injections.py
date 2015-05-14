"""`Factory` and `Singleton` providers with injections example."""

import sqlite3

from objects.providers import Singleton
from objects.providers import Factory

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
        return self.database.execute('SELECT 1').fetchone()[0]


# Database and `ObjectA` providers.
database = Singleton(sqlite3.Connection,
                     KwArg('database', ':memory:'),
                     KwArg('timeout', 30),
                     KwArg('detect_types', True),
                     KwArg('isolation_level', 'EXCLUSIVE'),
                     Attribute('row_factory', sqlite3.Row))

object_a_factory = Factory(ObjectA,
                           KwArg('database', database))

# Creating several `ObjectA` instances.
object_a_1 = object_a_factory()
object_a_2 = object_a_factory()

# Making some asserts.
assert object_a_1 is not object_a_2
assert object_a_1.database is object_a_2.database is database()
assert object_a_1.get_one() == object_a_2.get_one() == 1
