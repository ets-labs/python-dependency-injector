"""Custom `Factory` example."""

import dependency_injector.providers as providers


class User:
    """Example class User."""


class UsersFactory(providers.Provider):
    """Example users factory."""

    __slots__ = ('_factory',)

    def __init__(self):
        """Initialize instance."""
        self._factory = providers.Factory(User)
        super().__init__()

    def __call__(self, *args, **kwargs):
        """Return provided object.

        Callable interface implementation.
        """
        if self.last_overriding is not None:
            return self.last_overriding._provide(args, kwargs)
        return self._factory(*args, **kwargs)


# Users factory:
users_factory = UsersFactory()

# Creating several User objects:
user1 = users_factory()
user2 = users_factory()

# Making some asserts:
assert isinstance(user1, User)
assert isinstance(user2, User)
assert user1 is not user2
