"""
Concept example of objects catalogs.
"""

import objects
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
class Catalog(objects.Catalog):
    """
    Objects catalog.
    """

    database = objects.Singleton(provides=sqlite3.Connection,
                                 database='example.db')
    """ :type: (objects.Provider) -> sqlite3.Connection """

    object_a = objects.NewInstance(provides=A,
                                   db=database)
    """ :type: (objects.Provider) -> A """

    object_b = objects.NewInstance(provides=B,
                                   a=object_a,
                                   db=database)
    """ :type: (objects.Provider) -> B """


# Catalog injection into consumer class.
class Consumer(object):
    catalog = Catalog(Catalog.object_a,
                      Catalog.object_b)

    def return_a_b(self):
        return (self.catalog.object_a(),
                self.catalog.object_b())

a1, b1 = Consumer().return_a_b()


# Catalog static provides.
a2 = Catalog.object_a()
b2 = Catalog.object_b()

# Some asserts.
assert a1 is not a2
assert b1 is not b2
assert a1.db is a2.db is b1.db is b2.db
