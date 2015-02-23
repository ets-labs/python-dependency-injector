"""
Callable provider examples.
"""

from objects import AbstractCatalog
from objects.providers import (
    Singleton,
    Callable,
)
from objects.injections import (
    Injection,
    InitArg,
    Attribute,
)

import sqlite3


# Some example function.
def consuming_function(arg, db):
    return arg, db


# Catalog of objects providers.
class Catalog(AbstractCatalog):
    """
    Objects catalog.
    """

    database = Singleton(sqlite3.Connection,
                         InitArg('database', ':memory:'),
                         Attribute('row_factory', sqlite3.Row))
    """ :type: (objects.Provider) -> sqlite3.Connection """

    consuming_function = Callable(consuming_function,
                                  Injection('db', database))
    """ :type: (objects.Provider) -> consuming_function """


# Some calls.
arg1, db1 = Catalog.consuming_function(1)
arg2, db2 = Catalog.consuming_function(2)
arg3, db3 = Catalog.consuming_function(3)

# Some asserts.
assert db1 is db2 is db3
assert arg1 == 1
assert arg2 == 2
assert arg3 == 3
