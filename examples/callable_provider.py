"""Callable provider examples."""

from objects.catalog import AbstractCatalog

from objects.providers import Singleton
from objects.providers import Callable

from objects.injections import KwArg
from objects.injections import Attribute

import sqlite3


def consuming_function(arg, db):
    """Example function that has input arg and dependency on database."""
    return arg, db


class Catalog(AbstractCatalog):

    """Catalog of objects providers."""

    database = Singleton(sqlite3.Connection,
                         KwArg('database', ':memory:'),
                         Attribute('row_factory', sqlite3.Row))
    """:type: (objects.Provider) -> sqlite3.Connection"""

    consuming_function = Callable(consuming_function,
                                  KwArg('db', database))
    """:type: (objects.Provider) -> consuming_function"""


# Some calls.
arg1, db1 = Catalog.consuming_function(1)
arg2, db2 = Catalog.consuming_function(2)
arg3, db3 = Catalog.consuming_function(3)

# Some asserts.
assert db1 is db2 is db3
assert arg1 == 1
assert arg2 == 2
assert arg3 == 3
