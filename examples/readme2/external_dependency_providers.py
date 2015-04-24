"""External dependency providers example."""

import sqlite3

from objects.providers import Singleton
from objects.providers import NewInstance
from objects.providers import ExternalDependency

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
database = ExternalDependency(instance_of=sqlite3.Connection)

object_a = NewInstance(ObjectA,
                       KwArg('database', database))

# Satisfaction of external dependency.
database.override(Singleton(sqlite3.Connection,
                            KwArg('database', ':memory:'),
                            KwArg('timeout', 30),
                            KwArg('detect_types', True),
                            KwArg('isolation_level', 'EXCLUSIVE'),
                            Attribute('row_factory', sqlite3.Row)))

# Creating several `ObjectA` instances.
object_a_1 = object_a()
object_a_2 = object_a()

# Making some asserts.
assert object_a_1 is not object_a_2
assert object_a_1.database is object_a_2.database is database()
