"""Declarative IoC container's provider injections example."""

import sqlite3
import collections

import dependency_injector.containers as containers
import dependency_injector.providers as providers


UsersService = collections.namedtuple('UsersService', ['db'])
AuthService = collections.namedtuple('AuthService', ['db', 'users_service'])


class Services(containers.DeclarativeContainer):
    """IoC container of service providers."""

    database = providers.Singleton(sqlite3.connect, ':memory:')

    users = providers.Factory(UsersService,
                              db=database)

    auth = providers.Factory(AuthService,
                             db=database,
                             users_service=users)


# Retrieving service providers from container:
users_service = Services.users()
auth_service = Services.auth()

# Making some asserts:
assert users_service.db is auth_service.db is Services.database()
assert isinstance(auth_service.users_service, UsersService)
assert users_service is not Services.users()
assert auth_service is not Services.auth()
