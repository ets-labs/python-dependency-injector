"""Concept example of `Dependency Injector`."""

import sqlite3
import dependency_injector as di


class UsersService(object):
    """Users service, that has dependency on database."""

    def __init__(self, db):
        """Initializer."""
        self.db = db


class AuthService(object):
    """Auth service, that has dependencies on users service and database."""

    def __init__(self, db, users_service):
        """Initializer."""
        self.db = db
        self.users_service = users_service


class Services(di.AbstractCatalog):
    """Catalog of service providers."""

    database = di.Singleton(sqlite3.connect, ':memory:')
    """:type: di.Provider -> sqlite3.Connection"""

    users = di.Factory(UsersService,
                       db=database)
    """:type: di.Provider -> UsersService"""

    auth = di.Factory(AuthService,
                      db=database,
                      users_service=users)
    """:type: di.Provider -> AuthService"""


# Retrieving catalog providers:
users_service = Services.users()
auth_service = Services.auth()

# Making some asserts:
assert users_service.db is auth_service.db is Services.database()
assert isinstance(auth_service.users_service, UsersService)
assert users_service is not Services.users()
assert auth_service is not Services.auth()


# Making some "inline" injections:
@di.inject(users_service=Services.users)
@di.inject(auth_service=Services.auth)
@di.inject(database=Services.database)
def example(users_service, auth_service, database):
    """Example callback."""
    assert users_service.db is auth_service.db
    assert auth_service.db is database
    assert database is Services.database()


# Making a call of decorated callback:
example()
