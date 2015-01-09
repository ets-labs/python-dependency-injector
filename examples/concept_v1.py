"""
Concept example of objects catalogs.
"""

from objects import Catalog, Singleton, NewInstance, KwArg, Attribute
import sqlite3


# Some example classes.
class A(object):
    def __init__(self, db):
        self.db = db


class B(object):
    def __init__(self, a, db):
        self.a = a
        self.db = db


# Catalog of objects providers.
class AppCatalog(Catalog):
    """
    Objects catalog.
    """

    database = Singleton(provides=sqlite3.Connection,
                         database=KwArg('example.db'),
                         row_factory=Attribute(sqlite3.Row))
    """ :type: (Provider) -> sqlite3.Connection """

    object_a = NewInstance(provides=A,
                           db=KwArg(database))
    """ :type: (Provider) -> A """

    object_b = NewInstance(provides=B,
                           a=KwArg(object_a),
                           db=KwArg(database))
    """ :type: (Provider) -> B """


# Catalog injection into consumer class.
class Consumer(object):
    catalog = AppCatalog(AppCatalog.object_a,
                         AppCatalog.object_b)

    def return_a_b(self):
        return (self.catalog.object_a(),
                self.catalog.object_b())

a1, b1 = Consumer().return_a_b()


# Catalog static provides.
a2 = AppCatalog.object_a()
b2 = AppCatalog.object_b()

# Some asserts.
assert a1 is not a2
assert b1 is not b2
assert a1.db is a2.db is b1.db is b2.db
