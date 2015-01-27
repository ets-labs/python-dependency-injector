"""
Concept example of objects overrides.
"""


from objects import AbstractCatalog, overrides
from objects.providers import Singleton, NewInstance
from objects.injections import InitArg, Attribute

import sqlite3


# Some example class.
class ObjectA(object):
    def __init__(self, db):
        self.db = db


class ObjectAMock(ObjectA):
    pass


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


# Overriding Catalog by SandboxCatalog with some mocks.
@overrides(Catalog)
class SandboxCatalog(Catalog):
    """
    Sandbox objects catalog with some mocks.
    """

    object_a = NewInstance(ObjectAMock,
                           InitArg('db', Catalog.database))
    """ :type: (objects.Provider) -> ObjectA """


# Catalog static provides.
a1 = Catalog.object_a()
a2 = Catalog.object_a()

# Some asserts.
assert isinstance(a1, ObjectAMock)
assert isinstance(a2, ObjectAMock)
assert a1 is not a2
assert a1.db is a2.db is Catalog.database()
