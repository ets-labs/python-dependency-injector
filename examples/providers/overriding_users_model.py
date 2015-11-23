"""Overriding user's model example."""

from dependency_injector import providers


class User(object):
    """Example class User."""

    def __init__(self, id, password):
        """Initializer."""
        self.id = id
        self.password = password
        super(User, self).__init__()


class UserService(object):
    """Example class UserService."""

    def __init__(self, user_cls):
        """Initializer."""
        self.user_cls = user_cls
        super(UserService, self).__init__()

    def get_by_id(self, id):
        """Find user by his id and return user model."""
        return self.user_cls(id=id, password='secret' + str(id))

# Users factory and UserService provider:
users_service = providers.Factory(UserService, user_cls=User)

# Getting several users and making some asserts:
user1 = users_service().get_by_id(1)
user2 = users_service().get_by_id(2)

assert isinstance(user1, User)
assert user1.id == 1
assert user1.password == 'secret1'

assert isinstance(user2, User)
assert user2.id == 2
assert user2.password == 'secret2'

assert user1 is not user2

# Extending user model and user service for adding custom attributes without
# making any changes to client's code.


class ExtendedUser(User):
    """Example class ExtendedUser."""

    def __init__(self, id, password, first_name=None, last_name=None,
                 gender=None):
        """Initializer."""
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        super(ExtendedUser, self).__init__(id, password)


class ExtendedUserService(UserService):
    """Example class ExtendedUserService."""

    def get_by_id(self, id):
        """Find user by his id and return user model."""
        user = super(ExtendedUserService, self).get_by_id(id)
        user.first_name = 'John' + str(id)
        user.last_name = 'Smith' + str(id)
        user.gender = 'male'
        return user

# Overriding users_service provider:
extended_users_service = providers.Factory(ExtendedUserService,
                                           user_cls=ExtendedUser)
users_service.override(extended_users_service)

# Getting few other users users and making some asserts:
user3 = users_service().get_by_id(3)
user4 = users_service().get_by_id(4)

assert isinstance(user3, ExtendedUser)
assert user3.id == 3
assert user3.password == 'secret3'
assert user3.first_name == 'John3'
assert user3.last_name == 'Smith3'

assert isinstance(user4, ExtendedUser)
assert user4.id == 4
assert user4.password == 'secret4'
assert user4.first_name == 'John4'
assert user4.last_name == 'Smith4'

assert user3 is not user4
