"""`Dependency` providers example."""

import sqlite3
import contextlib

import dependency_injector.providers as providers


class UsersService:
    """Example class UsersService.

    UsersService has dependency on DBAPI 2.0 database connection.
    """

    def __init__(self, database):
        """Initialize instance.

        :param database: Database connection.
        :type database: sqlite3.dbapi2.Connection
        """
        self.database = database
        self.database.row_factory = sqlite3.dbapi2.Row

    def init_database(self):
        """Initialize database, if it has not been initialized yet."""
        with contextlib.closing(self.database.cursor()) as cursor:
            cursor.execute("""
              CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(32)
              )
            """)

    def create(self, name):
        """Create user with provided name and return his id."""
        with contextlib.closing(self.database.cursor()) as cursor:
            cursor.execute('INSERT INTO users(name) VALUES (?)', (name,))
            return cursor.lastrowid

    def get_by_id(self, id):
        """Return user info by user id."""
        with contextlib.closing(self.database.cursor()) as cursor:
            cursor.execute('SELECT id, name FROM users WHERE id=?', (id,))
            return cursor.fetchone()


# Database and UsersService providers:
database = providers.Dependency(instance_of=sqlite3.dbapi2.Connection)
users_service_factory = providers.Factory(UsersService,
                                          database=database)

# Out of library's scope.
#
# Setting database provider:
database.provided_by(providers.Singleton(sqlite3.dbapi2.Connection,
                                         database=':memory:',
                                         timeout=30,
                                         detect_types=True,
                                         isolation_level='EXCLUSIVE'))

# Creating UsersService instance:
users_service = users_service_factory()

# Initializing UsersService database:
users_service.init_database()

# Creating test user and retrieving full information about him:
test_user_id = users_service.create(name='test_user')
test_user = users_service.get_by_id(test_user_id)

# Making some asserts:
assert test_user['id'] == 1
assert test_user['name'] == 'test_user'
