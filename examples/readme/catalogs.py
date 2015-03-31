"""Catalogs example."""

import sqlite3
import httplib

from objects.catalog import AbstractCatalog

from objects.providers import Singleton
from objects.providers import NewInstance

from objects.injections import KwArg
from objects.injections import Attribute


class SomeModel(object):

    """SomeModel has dependency on database and api client.

    Dependencies need to be injected via init args.
    """

    def __init__(self, database, api_client):
        """Initializer."""
        self.database = database
        self.api_client = api_client

    def api_request(self):
        """Make api request."""
        self.api_client.request('GET', '/')
        return self.api_client.getresponse()

    def get_one(self):
        """Select one from database and return it."""
        return self.database.execute('SELECT 1').fetchone()[0]


class Resources(AbstractCatalog):

    """Resource providers catalog."""

    database = Singleton(sqlite3.Connection,
                         KwArg('database', ':memory:'),
                         KwArg('timeout', 30),
                         KwArg('detect_types', True),
                         KwArg('isolation_level', 'EXCLUSIVE'),
                         Attribute('row_factory', sqlite3.Row))

    api_client = Singleton(httplib.HTTPConnection,
                           KwArg('host', 'example.com'),
                           KwArg('port', 80),
                           KwArg('timeout', 10))


class Models(AbstractCatalog):

    """Model providers catalog."""

    some_model = NewInstance(SomeModel,
                             KwArg('database', Resources.database),
                             KwArg('api_client', Resources.api_client))


# Creating `SomeModel` instance.
some_model = Models.some_model()

# Making some asserts.
assert some_model.get_one() == 1
assert some_model.api_request().status == 200
