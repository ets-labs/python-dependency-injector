"""`Factory` providers example."""

import collections
import dependency_injector.providers as providers


User = collections.namedtuple('User', [])

# Factory provider creates new instance of specified class on every call.
users_factory = providers.Factory(User)

# Creating several User objects:
user1 = users_factory()  # Same as: user1 = User()
user2 = users_factory()  # Same as: user2 = User()
