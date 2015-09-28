"""`@di.inject()` decorator with classes example."""

import sqlite3
import flask
import flask.views
import dependency_injector as di


database = di.Singleton(sqlite3.Connection,
                        database=':memory:',
                        timeout=30,
                        detect_types=True,
                        isolation_level='EXCLUSIVE')

app = flask.Flask(__name__)


@di.inject(database=database)
@di.inject(some_setting=777)
class HelloView(flask.views.View):

    """Example flask class-based view."""

    def __init__(self, database, some_setting):
        """Initializer."""
        self.database = database
        self.some_setting = some_setting

    def dispatch_request(self):
        """Handle example request."""
        one = self.database.execute('SELECT 1').fetchone()[0]
        one *= self.some_setting
        return 'Query returned {0}, db connection {1}'.format(one, database)


app.add_url_rule('/', view_func=HelloView.as_view('hello_view'))

if __name__ == '__main__':
    app.run()

# Example output of "GET / HTTP/1.1" is:
# Query returned 777, db connection <sqlite3.Connection object at 0x1057e4030>
