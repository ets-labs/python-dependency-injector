"""Declarative catalog's provider injections example."""

import sqlite3

from dependency_injector import catalogs
from dependency_injector import providers


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


class Services(catalogs.DeclarativeCatalog):
    """Catalog of service providers."""

    database = providers.Singleton(sqlite3.connect, ':memory:')
    """:type: providers.Provider -> sqlite3.Connection"""

    users = providers.Factory(UsersService,
                              db=database)
    """:type: providers.Provider -> UsersService"""

    auth = providers.Factory(AuthService,
                             db=database,
                             users_service=users)
    """:type: providers.Provider -> AuthService"""


# Retrieving catalog providers:
users_service = Services.users()
auth_service = Services.auth()

# Making some asserts:
assert users_service.db is auth_service.db is Services.database()
assert isinstance(auth_service.users_service, UsersService)
assert users_service is not Services.users()
assert auth_service is not Services.auth()
