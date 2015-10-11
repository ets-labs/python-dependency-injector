"""`di.Singleton` providers example."""

import dependency_injector as di


class UserService(object):
    """Example class UserService."""

# Singleton provider creates new instance of specified class on first call and
# returns same instance on every next call.
users_service_provider = di.Singleton(UserService)

# Retrieving several UserService objects:
user_service1 = users_service_provider()
user_service2 = users_service_provider()

# Making some asserts:
assert user_service1 is user_service2
assert isinstance(user_service1, UserService)
assert isinstance(user_service2, UserService)
