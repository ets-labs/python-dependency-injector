"""Simple providers overriding example."""

import dependency_injector as di


class User(object):
    """Example class User."""

# Users factory:
users_factory = di.Factory(User)

# Creating several User objects:
user1 = users_factory()
user2 = users_factory()

# Making some asserts:
assert user1 is not user2
assert isinstance(user1, User) and isinstance(user2, User)


# Extending User:
class SuperUser(User):
    """Example class SuperUser."""

# Overriding users factory:
users_factory.override(di.Factory(SuperUser))

# Creating some more User objects using overridden users factory:
user3 = users_factory()
user4 = users_factory()

# Making some asserts:
assert user4 is not user3
assert isinstance(user3, SuperUser) and isinstance(user4, SuperUser)
