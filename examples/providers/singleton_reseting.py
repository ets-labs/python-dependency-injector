"""`Singleton` providers resetting example."""

import collections

import dependency_injector.providers as providers


UsersService = collections.namedtuple('UsersService', [])

# Users service singleton provider:
users_service_provider = providers.Singleton(UsersService)

# Retrieving several UsersService objects:
users_service1 = users_service_provider()
users_service2 = users_service_provider()

# Making some asserts:
assert users_service1 is users_service2

# Resetting of memorized instance:
users_service_provider.reset()

# Retrieving one more UserService object:
users_service3 = users_service_provider()

# Making some asserts:
assert users_service3 is not users_service1
