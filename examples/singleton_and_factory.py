"""Providers delegation example."""

from objects.providers import Factory
from objects.providers import Singleton
from objects.providers import Delegate

from objects.injections import KwArg


class User(object):

    """Example class User."""

    def __init__(self, id, name):
        """Initializer.

        :param id: int
        :param name: str
        :return:
        """
        self.id = id
        self.name = name


class UserService(object):

    """Example class UserService.

    UserService has dependency on users factory.
    """

    def __init__(self, users_factory):
        """Initializer.

        :param users_factory: objects.providers.Factory
        :return:
        """
        self.users_factory = users_factory

    def get_by_id(self, id):
        """Return user info by user id."""
        return self.users_factory(id=id, name=self._get_name_from_db(id))

    def _get_name_from_db(self, id):
        """Return user's name from database by his id.

        Main purpose of this method is just to show the fact of retrieving
        some user's data from database, so, actually, it simulates work
        with database just by merging constant string with provided user's id.
        """
        return ''.join(('user', str(id)))


# Users factory and UserService provider:
users_service = Singleton(UserService,
                          KwArg('users_factory',
                                Delegate(Factory(User))))


# Creating several User objects:
user1 = users_service().get_by_id(1)
user2 = users_service().get_by_id(2)

# Making some asserts:
assert user1.id == 1
assert user1.name == 'user1'

assert user2.id == 2
assert user2.name == 'user2'
