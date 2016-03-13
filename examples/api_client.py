"""Pythonic way for Dependency Injection - API Client."""

from dependency_injector import providers

from mock import Mock


class ApiClient(object):
    """Some API client."""

    def __init__(self, host, api_key):
        """Initializer."""
        self.host = host
        self.api_key = api_key

    def call(self, operation, data):
        """Make some network operations."""
        print 'API call [{0}:{1}], method - {2}, data - {3}'.format(
            self.host, self.api_key, operation, repr(data))


class User(object):
    """User model."""

    def __init__(self, id, api_client):
        """Initializer."""
        self.id = id
        self.api_client = api_client

    def register(self):
        """Register user."""
        self.api_client.call('register', {'id': self.id})


# Creating ApiClient and User providers:
api_client = providers.Singleton(ApiClient,
                                 host='production.com',
                                 api_key='PROD_API_KEY')
user_factory = providers.Factory(User,
                                 api_client=api_client)

# Creating several users and register them:
user1 = user_factory(1)
user1.register()
# API call [production.com:PROD_API_KEY], method - register, data - {'id': 1}

user2 = user_factory(2)
user2.register()
# API call [production.com:PROD_API_KEY], method - register, data - {'id': 2}

# Mock ApiClient for testing:
with api_client.override(Mock(ApiClient)) as api_client_mock:
    user = user_factory('test')
    user.register()
    api_client_mock().call.assert_called_with('register', {'id': 'test'})


# Overriding of ApiClient on dev environment:
api_client.override(providers.Singleton(ApiClient,
                                        host='localhost',
                                        api_key='DEV_API_KEY'))

user3 = user_factory(3)
user3.register()
# API call [localhost:DEV_API_KEY], method - register, data - {'id': 3}
