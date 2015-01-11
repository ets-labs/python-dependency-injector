"""
Concept example of objects overrides.
"""


from objects import Catalog, Singleton, NewInstance, InitArg, Attribute, overrides
import sqlite3


# Some example class.
class ObjectA(object):
    def __init__(self, db):
        self.db = db


class ObjectAMock(ObjectA):
    pass


# Catalog of objects providers.
class AppCatalog(Catalog):
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


# Overriding AppCatalog by SandboxCatalog with some mocks.
@overrides(AppCatalog)
class SandboxCatalog(AppCatalog):
    """
    Sandbox objects catalog with some mocks.
    """

    object_a = NewInstance(ObjectAMock,
                           InitArg('db', AppCatalog.database))
    """ :type: (objects.Provider) -> ObjectA """


# Catalog static provides.
a1 = AppCatalog.object_a()
a2 = AppCatalog.object_a()

# Some asserts.
assert isinstance(a1, ObjectAMock)
assert isinstance(a2, ObjectAMock)
assert a1 is not a2
assert a1.db is a2.db is AppCatalog.database()
