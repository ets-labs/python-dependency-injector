"""
Concept example of objects catalogs.
"""

from objects import AbstractCatalog
from objects.providers import Singleton
from objects.providers import NewInstance
from objects.providers import ExternalDependency
from objects.injections import InitArg
from objects.injections import Attribute

import sqlite3


# Some example classes.
class ObjectA(object):
    def __init__(self, db):
        self.db = db


class ObjectB(object):
    def __init__(self, a, db):
        self.a = a
        self.db = db


# Catalog of objects providers.
class Catalog(AbstractCatalog):
    """
    Objects catalog.
    """

    database = ExternalDependency(instance_of=sqlite3.Connection)
    """ :type: (objects.Provider) -> sqlite3.Connection """

    object_a = NewInstance(ObjectA,
                           InitArg('db', database))
    """ :type: (objects.Provider) -> ObjectA """

    object_b = NewInstance(ObjectB,
                           InitArg('a', object_a),
                           InitArg('db', database))
    """ :type: (objects.Provider) -> ObjectB """


# Satisfaction of external dependency.
Catalog.database.satisfy(Singleton(sqlite3.Connection,
                                   InitArg('database', ':memory:'),
                                   Attribute('row_factory', sqlite3.Row)))

# Catalog static provides.
a1, a2 = Catalog.object_a(), Catalog.object_a()
b1, b2 = Catalog.object_b(), Catalog.object_b()

# Some asserts.
assert a1 is not a2
assert b1 is not b2
assert a1.db is a2.db is b1.db is b2.db is Catalog.database()
