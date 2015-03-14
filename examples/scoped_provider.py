"""Scoped provider examples."""

from objects import AbstractCatalog

from objects.providers import Singleton
from objects.providers import Scoped

from objects.injections import InitArg
from objects.injections import Attribute

import sqlite3


class ObjectA(object):

    """Example class ObjectA, that has dependency on database."""

    def __init__(self, db):
        """Initializer."""
        self.db = db


class Catalog(AbstractCatalog):

    """Catalog of objects providers."""

    database = Singleton(sqlite3.Connection,
                         InitArg('database', ':memory:'),
                         Attribute('row_factory', sqlite3.Row))
    """:type: (objects.Provider) -> sqlite3.Connection"""

    object_a = Scoped(ObjectA,
                      InitArg('db', database))
    """:type: (objects.Provider) -> ObjectA"""


# Making one more scope using provider methods.
Catalog.object_a.in_scope('request')

object_a1 = Catalog.object_a()
object_a2 = Catalog.object_a()

Catalog.object_a.out_of_scope('request')

assert object_a1 is object_a2
assert object_a1.db is object_a2.db
