"""`di.Singleton` providers resetting example."""

import dependency_injector as di


class UserService(object):

    """Example class UserService."""

# Users service singleton provider:
users_service_provider = di.Singleton(UserService)

# Retrieving several UserService objects:
user_service1 = users_service_provider()
user_service2 = users_service_provider()

# Making some asserts:
assert user_service1 is user_service2
assert isinstance(user_service1, UserService)
assert isinstance(user_service2, UserService)

# Resetting of memorized instance:
users_service_provider.reset()

# Retrieving one more UserService object:
user_service3 = users_service_provider()

# Making some asserts:
assert user_service3 is not user_service1
