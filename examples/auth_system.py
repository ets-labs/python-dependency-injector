"""Pythonic way for Dependency Injection."""

from dependency_injector import providers
from dependency_injector import injections


@providers.DelegatedCallable
def get_user_info(user_id):
    """Return user info."""
    raise NotImplementedError()


@providers.Factory
@injections.inject(get_user_info=get_user_info)
class AuthComponent(object):
    """Some authentication component."""

    def __init__(self, get_user_info):
        """Initializer."""
        self.get_user_info = get_user_info

    def authenticate_user(self, token):
        """Authenticate user by token."""
        user_info = self.get_user_info(user_id=token + '1')
        return user_info


print AuthComponent
print get_user_info


@get_user_info.override
@providers.DelegatedCallable
def get_user_info(user_id):
    """Return user info."""
    return {'user_id': user_id}


print AuthComponent().authenticate_user(token='abc')
# {'user_id': 'abc1'}
