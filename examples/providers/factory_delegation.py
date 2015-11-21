"""`Factory` providers delegation example."""

from dependency_injector import providers


class User(object):
    """Example class User."""

    def __init__(self, photos_factory):
        """Initializer.

        :param photos_factory: providers.Factory -> Photo
        """
        self.photos_factory = photos_factory
        self._main_photo = None
        super(User, self).__init__()

    @property
    def main_photo(self):
        """Return user's main photo."""
        if not self._main_photo:
            self._main_photo = self.photos_factory()
        return self._main_photo


class Photo(object):
    """Example class Photo."""

# User and Photo factories:
photos_factory = providers.Factory(Photo)
users_factory = providers.Factory(User,
                                  photos_factory=photos_factory.delegate())

# Creating several User objects:
user1 = users_factory()
user2 = users_factory()

# Making some asserts:
assert isinstance(user1, User)
assert isinstance(user1.main_photo, Photo)

assert isinstance(user2, User)
assert isinstance(user2.main_photo, Photo)

assert user1 is not user2
assert user1.main_photo is not user2.main_photo
