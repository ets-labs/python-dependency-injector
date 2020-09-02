"""Simple providers overriding example."""

import unittest.mock

from dependency_injector import providers


class ApiClient:
    ...


class ApiClientStub(ApiClient):
    ...


class Service:
    def __init__(self, api_client: ApiClient):
        self._api_client = api_client


api_client_factory = providers.Factory(ApiClient)
service_factory = providers.Factory(
    Service,
    api_client=api_client_factory,
)


if __name__ == '__main__':
    # 1. Use .override() to replace the API client with stub
    api_client_factory.override(providers.Factory(ApiClientStub))
    service1 = service_factory()
    assert isinstance(service1.api_client, ApiClientStub)

    # 2. Use .override() as a context manager to mock the API client in testing
    with api_client_factory.override(unittest.mock.Mock(ApiClient)):
        service3 = service_factory()
        assert isinstance(service3.api_client, unittest.mock.Mock)

    # 3. Use .reset_override() to get back to normal
    api_client_factory.reset_override()
    service3 = service_factory()
    assert isinstance(service3.api_client, ApiClient)
