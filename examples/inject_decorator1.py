"""`@inject` decorator example.

Flask is required to make this example work.
"""

import sqlite3

from flask import Flask

from objects.providers import Factory
from objects.providers import Singleton
from objects.injections import KwArg
from objects.injections import Attribute
from objects.decorators import inject


class ObjectA(object):

    """ObjectA has dependency on database."""

    def __init__(self, database):
        """Initializer.

        Database dependency need to be injected via init arg."""
        self.database = database

    def get_one(self):
        """Select one from database and return it."""
        return self.database.execute('SELECT 1').fetchone()[0]


# Database and `ObjectA` providers.
database = Singleton(sqlite3.Connection,
                     KwArg('database', ':memory:'),
                     KwArg('timeout', 30),
                     KwArg('detect_types', True),
                     KwArg('isolation_level', 'EXCLUSIVE'),
                     Attribute('row_factory', sqlite3.Row))

object_a_factory = Factory(ObjectA,
                           KwArg('database', database))


# Flask application.
app = Flask(__name__)


# Flask view with inject decorator.
@app.route('/')
@inject(KwArg('database', database))
@inject(KwArg('object_a', object_a_factory))
def hello(database):
    one = database.execute('SELECT 1').fetchone()[0]
    return 'Query returned {0}, db connection {1}'.format(one, database)


if __name__ == '__main__':
    app.run()

# Example output of "GET / HTTP/1.1" is:
# Query returned 1, db connection <sqlite3.Connection object at 0x1057e4030>
