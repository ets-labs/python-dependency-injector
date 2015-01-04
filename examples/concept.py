"""
Concept example of objects catalogs.
"""

import objects
import sqlite3


class A(object):
    def __init__(self, db):
        self.db = db


class B(object):
    def __init__(self, a, db):
        self.a = a
        self.db = db


class Catalog(objects.Catalog):
    """
    Objects catalog.
    """

    database = objects.Singleton(sqlite3.Connection,
                                 database='example.db')
    """ :type: (objects.Provider) -> sqlite3.Connection """

    object_a = objects.NewInstance(A,
                                   db=database)
    """ :type: (objects.Provider) -> A """

    object_b = objects.NewInstance(B,
                                   a=object_a,
                                   db=database)
    """ :type: (objects.Provider) -> B """


catalog = Catalog(Catalog.object_a,
                  Catalog.object_b)
a1 = catalog.object_a()
b1 = catalog.object_b()

a2 = Catalog.object_a()
b2 = Catalog.object_b()

print a1, a1.db
print a2, a2.db
print b1, b1.db
print b2, b2.db

assert a1 is not a2
assert b1 is not b2
