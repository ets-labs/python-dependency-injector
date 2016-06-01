"""Main module."""

import core
import services
import container

from dependency_injector import providers
from dependency_injector import errors


if __name__ == '__main__':
    # Creating users & auth services:
    users_service = container.Services.users()
    auth_service = container.Services.auth()

    # Making some asserts:
    assert users_service.config == {'option1': '111',
                                    'option2': '222'}
    assert auth_service.config == {'option3': '333',
                                   'option4': '444'}
    assert isinstance(auth_service.users_service, services.UsersService)

    # Trying to declare services container with other provider type:
    try:
        class _Services1(core.ServicesContainer):

            users = providers.Factory(services.UsersService)
    except errors.Error as exception:
        print exception
        # <class '__main__._Services1'> can contain only
        # <class 'core.ServiceProvider'> instances

    # Trying to declare services container with correct provider by invalid
    # provided type:
    try:
        class _Services2(core.ServicesContainer):

            users = core.ServiceProvider(object)
    except errors.Error as exception:
        print exception
        # <class 'core.ServiceProvider'> can provide only
        # <class 'core.BaseService'> instances
