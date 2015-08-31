"""`@inject` decorator and Flask view example."""

import sqlite3

from flask import Flask

from dependency_injector.providers import Singleton
from dependency_injector.injections import KwArg
from dependency_injector.injections import Attribute
from dependency_injector.injections import inject


# Database and `ObjectA` providers.
database = Singleton(sqlite3.Connection,
                     KwArg('database', ':memory:'),
                     KwArg('timeout', 30),
                     KwArg('detect_types', True),
                     KwArg('isolation_level', 'EXCLUSIVE'),
                     Attribute('row_factory', sqlite3.Row))

# Flask application:
app = Flask(__name__)


# Flask view with @inject decorator:
@app.route('/')
@inject(KwArg('database', database))
def hello(database):
    """Example Flask view."""
    one = database.execute('SELECT 1').fetchone()[0]
    return 'Query returned {0}, db connection {1}'.format(one, database)


if __name__ == '__main__':
    app.run()

# Example output of "GET / HTTP/1.1" is:
# Query returned 1, db connection <sqlite3.Connection object at 0x1057e4030>
