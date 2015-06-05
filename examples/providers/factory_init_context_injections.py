"""`Factory` providers with init injections and context arguments example."""

from objects.providers import Factory
from objects.injections import KwArg


class User(object):

    """Example class User."""

    def __init__(self, id, main_photo):
        """Initializer.

        :param id: int
        :param main_photo: Photo
        :return:
        """
        self.id = id
        self.main_photo = main_photo
        super(User, self).__init__()


class Photo(object):

    """Example class Photo."""


# User and Photo factories:
photos_factory = Factory(Photo)
users_factory = Factory(User,
                        KwArg('main_photo', photos_factory))

# Creating several User objects:
user1 = users_factory(1)  # Same as: User(1, main_photo=Photo())
user2 = users_factory(2)  # Same as: User(1, main_photo=Photo())

# Making some asserts:
assert user1.id == 1
assert user2.id == 2
assert user1 is not user2
assert isinstance(user1.main_photo, Photo)
assert isinstance(user2.main_photo, Photo)
assert user1.main_photo is not user2.main_photo

# Context keyword arguments have priority on KwArg injections priority:
photo_mock = Photo()

user3 = users_factory(3, main_photo=photo_mock)

assert user3.id == 3
assert user3 not in (user2, user1)
assert user3.main_photo is photo_mock
