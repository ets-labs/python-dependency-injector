"""`Singleton` providers example."""

import collections

import dependency_injector.providers as providers


UsersService = collections.namedtuple('UsersService', [])

# Singleton provider creates new instance of specified class on first call
# and returns same instance on every next call.
users_service_provider = providers.Singleton(UsersService)

# Retrieving several UserService objects:
users_service1 = users_service_provider()
users_service2 = users_service_provider()

# Making some asserts:
assert users_service1 is users_service2
