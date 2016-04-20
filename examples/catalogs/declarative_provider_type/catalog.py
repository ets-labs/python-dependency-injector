"""Specialized declarative catalog example."""

import services

from dependency_injector import providers
from dependency_injector import errors


class UsersService(services.Base):
    """Users service."""

    def __init__(self, config):
        """Initializer."""
        self.config = config
        super(UsersService, self).__init__()


class AuthService(services.Base):
    """Auth service."""

    def __init__(self, config, users_service):
        """Initializer."""
        self.config = config
        self.users_service = users_service
        super(AuthService, self).__init__()


class Services(services.Catalog):
    """Services catalog."""

    users = services.Provider(UsersService,
                              config={'option1': '111',
                                      'option2': '222'})

    auth = services.Provider(AuthService,
                             config={'option3': '333',
                                     'option4': '444'},
                             users_service=users)


# Creating users & auth services:
users_service = Services.users()
auth_service = Services.auth()

# Making some asserts:
assert users_service.config == {'option1': '111',
                                'option2': '222'}
assert auth_service.config == {'option3': '333',
                               'option4': '444'}
assert isinstance(auth_service.users_service, UsersService)

# Trying to declare services catalog with other provider type:
try:
    class Services1(services.Catalog):
        """Services catalog."""

        users = providers.Factory(UsersService)
except errors.Error as exception:
    print exception
    # <__main__.Services1()> can contain only <class 'services.Provider'>
    # instances

# Trying to declare services catalog with correct provider by invalid provided
# type:
try:
    class Services2(services.Catalog):
        """Services catalog."""

        users = services.Provider(object)
except errors.Error as exception:
    print exception
    # <class 'services.Provider'> can provide only <class 'services.Base'>
    # instances
