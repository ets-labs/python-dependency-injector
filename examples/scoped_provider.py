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


# Making scope using `with` statement.
with Catalog.object_a as object_a_provider:
    object_a1 = object_a_provider()
    object_a2 = object_a_provider()

    assert object_a1 is object_a2
    assert object_a1.db is object_a2.db

# Making another one scope using `with` statement.
with Catalog.object_a as object_a_provider:
    object_a3 = object_a_provider()
    object_a4 = object_a_provider()

    assert object_a3 is object_a4
    assert object_a3.db is object_a4.db

    assert (object_a1 is not object_a3) and \
           (object_a1 is not object_a4)
    assert (object_a2 is not object_a3) and \
           (object_a2 is not object_a4)


# Making one more scope using provider methods.
Catalog.object_a.in_scope()

object_a5 = Catalog.object_a()
object_a6 = Catalog.object_a()

Catalog.object_a.out_of_scope()

assert object_a5 is object_a6
assert object_a5.db is object_a6.db

assert (object_a1 is not object_a3) and \
       (object_a1 is not object_a4) and \
       (object_a1 is not object_a5) and \
       (object_a1 is not object_a6)
assert (object_a2 is not object_a3) and \
       (object_a2 is not object_a4) and \
       (object_a2 is not object_a5) and \
       (object_a2 is not object_a6)
