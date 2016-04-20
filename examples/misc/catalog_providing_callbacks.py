"""Pythonic way for Dependency Injection - Providing Callbacks Catalog."""

import sqlite3

from dependency_injector import catalogs
from dependency_injector import providers
from dependency_injector import injections


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

    @providers.Singleton
    def database():
        """Provide database connection.

        :rtype: providers.Provider -> sqlite3.Connection
        """
        return sqlite3.connect(':memory:')

    @providers.Factory
    @injections.inject(db=database)
    def users(**kwargs):
        """Provide users service.

        :rtype: providers.Provider -> UsersService
        """
        return UsersService(**kwargs)

    @providers.Factory
    @injections.inject(db=database)
    @injections.inject(users_service=users)
    def auth(**kwargs):
        """Provide users service.

        :rtype: providers.Provider -> AuthService
        """
        return AuthService(**kwargs)


# Retrieving catalog providers:
users_service = Services.users()
auth_service = Services.auth()

# Making some asserts:
assert users_service.db is auth_service.db is Services.database()
assert isinstance(auth_service.users_service, UsersService)
assert users_service is not Services.users()
assert auth_service is not Services.auth()
