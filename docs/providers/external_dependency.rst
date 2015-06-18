External dependency providers
-----------------------------

``ExternalDependency`` provider can be useful for development of
self-sufficient libraries / modules / applications that has required external
dependencies.

For example, you have created self-sufficient library / module / application,
that has dependency on *database connection*.

Second step you want to do is to make this software component to be easy
reusable by wide amount of developers and to be easily integrated into many
applications.

It may be good idea, to move all external dependencies (like
*database connection*) to the top level and make them to be injected on your
software component's initialization. It will make third party developers feel
themselves free about integration of yours component in their applications,
because they would be able to find right place / right way for doing this
in their application's architectures.

At the same time, you can be sure, that your external dependency will be
satisfied by appropriate instance.


Example:


.. note::

    Class ``UserService`` is a part of some library. ``UserService`` has
    dependency on database connection, which can be satisfied with any
    DBAPI 2.0 database connection. Being a self-sufficient library,
    ``UserService`` doesn't hardcode any kind of database management logic.
    Instead of this, ``UserService`` provides external dependency, that has to
    be satisfied out of library's scope.

.. image:: /images/external_dependency.png

.. code-block:: python

    """`ExternalDependency` providers example."""

    from objects.providers import ExternalDependency
    from objects.providers import Factory
    from objects.providers import Singleton

    from objects.injections import KwArg
    from objects.injections import Attribute

    # Importing SQLITE3 and contextlib.closing for working with cursors:
    import sqlite3
    from contextlib import closing


    # Definition of example UserService:
    class UserService(object):

        """Example class UserService.

        UserService has dependency on DBAPI 2.0 database connection."""

        def __init__(self, database):
            """Initializer.

            Database dependency need to be injected via init arg."""
            self.database = database

        def init_database(self):
            """Initialize database, if it has not been initialized yet."""
            with closing(self.database.cursor()) as cursor:
                cursor.execute("""
                  CREATE TABLE IF NOT EXISTS users(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name VARCHAR(32)
                  )
                """)

        def create(self, name):
            """Create user with provided name and return his id."""
            with closing(self.database.cursor()) as cursor:
                cursor.execute('INSERT INTO users(name) VALUES (?)', (name,))
                return cursor.lastrowid

        def get_by_id(self, id):
            """Return user info by user id."""
            with closing(self.database.cursor()) as cursor:
                cursor.execute('SELECT id, name FROM users WHERE id=?', (id,))
                return cursor.fetchone()


    # Database and UserService providers:
    database = ExternalDependency(instance_of=sqlite3.Connection)
    users_service_factory = Factory(UserService,
                                    KwArg('database', database))

    # Out of library's scope.
    #
    # Setting database provider:
    database.provided_by(Singleton(sqlite3.Connection,
                                   KwArg('database', ':memory:'),
                                   KwArg('timeout', 30),
                                   KwArg('detect_types', True),
                                   KwArg('isolation_level', 'EXCLUSIVE'),
                                   Attribute('row_factory', sqlite3.Row)))

    # Creating UserService instance:
    users_service = users_service_factory()

    # Initializing UserService database:
    users_service.init_database()

    # Creating test user and retrieving full information about him:
    test_user_id = users_service.create(name='test_user')
    test_user = users_service.get_by_id(test_user_id)

    # Making some asserts:
    assert test_user['id'] == 1
    assert test_user['name'] == 'test_user'

