"""`Factory` providers delegation example."""

import collections

import dependency_injector.providers as providers


Photo = collections.namedtuple('Photo', [])


class User(object):
    """Example user model."""

    def __init__(self, photos_factory):
        """Initialize instance."""
        self.photos_factory = photos_factory
        self._main_photo = None

    @property
    def main_photo(self):
        """Return user's main photo."""
        if not self._main_photo:
            self._main_photo = self.photos_factory()
        return self._main_photo


# Defining User and Photo factories using DelegatedFactory provider:
photos_factory = providers.DelegatedFactory(Photo)
users_factory = providers.DelegatedFactory(User,
                                           photos_factory=photos_factory)

# or using Delegate(Factory(...))

photos_factory = providers.Factory(Photo)
users_factory = providers.Factory(User,
                                  photos_factory=providers.Delegate(
                                      photos_factory))


# or using Factory(...).delegate()

photos_factory = providers.Factory(Photo)
users_factory = providers.Factory(User,
                                  photos_factory=photos_factory.delegate())


# Creating several User objects:
user1 = users_factory()  # Same as: user1 = User(photos_factory=photos_factory)
user2 = users_factory()  # Same as: user2 = User(photos_factory=photos_factory)

# Making some asserts:
assert isinstance(user1.main_photo, Photo)
assert isinstance(user2.main_photo, Photo)

# or using Factory(...).provider

photos_factory = providers.Factory(Photo)
users_factory = providers.Factory(User,
                                  photos_factory=photos_factory.provider)


# Creating several User objects:
user1 = users_factory()  # Same as: user1 = User(photos_factory=photos_factory)
user2 = users_factory()  # Same as: user2 = User(photos_factory=photos_factory)

# Making some asserts:
assert isinstance(user1.main_photo, Photo)
assert isinstance(user2.main_photo, Photo)
