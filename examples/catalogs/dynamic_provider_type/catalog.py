"""Specialized dynamic catalog example."""

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


services_catalog = services.Catalog()
services_catalog.users = services.Provider(UsersService,
                                           config={'option1': '111',
                                                   'option2': '222'})
services_catalog.auth = services.Provider(AuthService,
                                          config={'option3': '333',
                                                  'option4': '444'},
                                          users_service=services_catalog.users)

# Creating users & auth services:
users_service = services_catalog.users()
auth_service = services_catalog.auth()

# Making some asserts:
assert users_service.config == {'option1': '111',
                                'option2': '222'}
assert auth_service.config == {'option3': '333',
                               'option4': '444'}
assert isinstance(auth_service.users_service, UsersService)

# Trying to declare services catalog with other provider type:
try:
    services_catalog.users = providers.Factory(UsersService)
except errors.Error as exception:
    print exception
    # <services.Catalog(users, auth)> can contain only
    # <class 'services.Provider'> instances

# Trying to declare services catalog with correct provider by invalid provided
# type:
try:
    services_catalog.users = services.Provider(object)
except errors.Error as exception:
    print exception
    # <class 'services.Provider'> can provide only <class 'services.Base'>
    # instances
