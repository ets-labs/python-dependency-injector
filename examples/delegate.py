"""
Example of providers delegate.
"""

from objects import AbstractCatalog
from objects.providers import Singleton
from objects.providers import NewInstance
from objects.injections import InitArg
from objects.injections import Attribute


import sqlite3


# Some example classes.
class ObjectA(object):
    def __init__(self, db):
        self.db = db


class ObjectB(object):
    def __init__(self, a_factory):
        self.a_factory = a_factory


# Catalog of objects providers.
class Catalog(AbstractCatalog):
    """
    Objects catalog.
    """

    database = Singleton(sqlite3.Connection,
                         InitArg('database', ':memory:'),
                         Attribute('row_factory', sqlite3.Row))
    """ :type: (objects.Provider) -> sqlite3.Connection """

    object_a = NewInstance(ObjectA,
                           InitArg('db', database))
    """ :type: (objects.Provider) -> ObjectA """

    object_b = Singleton(ObjectB,
                         InitArg('a_factory', object_a.delegate()))
    """ :type: (objects.Provider) -> ObjectB """


# Catalog static provides.
b = Catalog.object_b()
a1, a2 = b.a_factory(), b.a_factory()

# Some asserts.
assert a1 is not a2
assert a1.db is a2.db is Catalog.database()
