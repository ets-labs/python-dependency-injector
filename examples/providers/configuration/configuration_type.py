"""`Configuration` provider type specification example."""

import os

from dependency_injector import providers


class ApiClient:
    def __init__(self, api_key: str, timeout: int):
        self.api_key = api_key
        self.timeout = timeout


config = providers.Configuration()

api_client_factory = providers.Factory(
    ApiClient,
    api_key=config.api.key,
    timeout=config.api.timeout.as_int(),
)


if __name__ == '__main__':
    # Emulate environment variables
    os.environ['API_KEY'] = 'secret'
    os.environ['API_TIMEOUT'] = '5'

    config.api.key.from_env('API_KEY')
    config.api.timeout.from_env('API_TIMEOUT')

    api_client = api_client_factory()

    assert api_client.api_key == 'secret'
    assert api_client.timeout == 5
