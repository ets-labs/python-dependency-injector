"""`Callable` provider examples."""

from objects.providers import Callable
from objects.providers import Singleton

from objects.injections import KwArg

import sqlite3


def some_function(arg, database):
    """Example function that has input arg and dependency on database."""
    return database.execute('SELECT @1', [arg]).fetchone()[0]


# Database and `ObjectA` providers.
database = Singleton(sqlite3.Connection,
                     KwArg('database', ':memory:'))

some_function = Callable(some_function,
                         KwArg('database', database))

# Some asserts.
assert some_function(1) == 1
assert some_function(2) == 2
assert some_function(2231) == 2231
