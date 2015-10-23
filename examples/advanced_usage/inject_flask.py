"""`@di.inject()` decorator and Flask view example."""

import sqlite3
import flask
import dependency_injector as di


database = di.Singleton(sqlite3.connect,
                        ':memory:',
                        timeout=30,
                        detect_types=True,
                        isolation_level='EXCLUSIVE')

app = flask.Flask(__name__)


@app.route('/')
@di.inject(database)
@di.inject(flask.request)
def hello(request, database):
    """Example Flask view."""
    print request
    one = database.execute('SELECT 1').fetchone()[0]
    return 'Query returned {0}, db connection {1}'.format(one, database)


if __name__ == '__main__':
    app.run()

# Example output of "GET / HTTP/1.1" is:
# Query returned 1, db connection <sqlite3.Connection object at 0x1057e4030>
