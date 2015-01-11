"""
Concept example of objects injections.
"""

from objects import Catalog, Singleton, NewInstance, InitArg, Attribute, inject
import sqlite3


# Some example class.
class ObjectA(object):
    def __init__(self, db):
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


# Class attributes injections.
@inject(Attribute('a', AppCatalog.object_a))
@inject(Attribute('database', AppCatalog.database))
class Consumer(object):
    """
    Some consumer class with database dependency via attribute.
    """

    a = None
    """ :type: (objects.Provider) -> ObjectA """

    database = None
    """ :type: (objects.Provider) -> sqlite3.Connection """

    def tests(self):
        a1, a2 = self.a(), self.a()

        assert a1 is not a2
        assert a1.db is a2.db is self.database()


consumer = Consumer()
consumer.tests()


# Class __init__ injections.
@inject(InitArg('a1', AppCatalog.object_a))
@inject(InitArg('a2', AppCatalog.object_a))
@inject(InitArg('database', AppCatalog.database))
class ConsumerWithInitArg(object):
    """
    Some consumer class with database dependency via init arg.
    """

    def __init__(self, a1, a2, database):
        """
        Initializer.

        :param a1: ObjectA
        :param a2: ObjectA
        :param database: sqlite3.Connection
        """
        self.a1 = a1
        self.a2 = a2
        self.database = database

    def tests(self):
        assert self.a1 is not self.a2
        assert self.a1.db is self.a2.db is self.database


consumer = ConsumerWithInitArg()
consumer.tests()
