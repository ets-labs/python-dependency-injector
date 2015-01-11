"""
Concept example of objects catalogs.
"""

from objects import Catalog, Singleton, NewInstance, InitArg, Attribute
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

    object_b = NewInstance(ObjectB,
                           InitArg('a', object_a),
                           InitArg('db', database))
    """ :type: (objects.Provider) -> ObjectB """


# Catalog static provides.
a1, a2 = AppCatalog.object_a(), AppCatalog.object_a()
b1, b2 = AppCatalog.object_b(), AppCatalog.object_b()

# Some asserts.
assert a1 is not a2
assert b1 is not b2
assert a1.db is a2.db is b1.db is b2.db is AppCatalog.database()


# Dependency injection (The Python Way) into class.
class Consumer(object):

    dependencies = AppCatalog(AppCatalog.object_a,
                              AppCatalog.object_b)

    def test(self):
        a1 = self.dependencies.object_a()
        a2 = self.dependencies.object_a()

        b1 = self.dependencies.object_b()
        b2 = self.dependencies.object_b()

        # Some asserts.
        assert a1 is not a2
        assert b1 is not b2
        assert a1.db is a2.db is b1.db is b2.db

        try:
            self.dependencies.database()
        except AttributeError:
            pass
        else:
            raise Exception('Database is not listed as a dependency')

Consumer().test()


# Dependency injection (The Python Way) into a callback.
def consumer_callback(dependencies=AppCatalog(AppCatalog.object_a,
                                              AppCatalog.object_b)):
    a1 = dependencies.object_a()
    a2 = dependencies.object_a()

    b1 = dependencies.object_b()
    b2 = dependencies.object_b()

    # Some asserts.
    assert a1 is not a2
    assert b1 is not b2
    assert a1.db is a2.db is b1.db is b2.db

    try:
        dependencies.database()
    except AttributeError:
        pass
    else:
        raise Exception('Database is not listed as a dependency')
