"""Simple providers overriding example."""

import dataclasses
import unittest.mock

from dependency_injector import containers, providers


class ApiClient:
    ...


class ApiClientStub(ApiClient):
    ...


@dataclasses.dataclass
class Service:
    api_client: ApiClient


class Container(containers.DeclarativeContainer):

    api_client_factory = providers.Factory(ApiClient)

    service_factory = providers.Factory(
        Service,
        api_client=api_client_factory,
    )


if __name__ == "__main__":
    container = Container()

    # 1. Use .override() to replace the API client with stub
    container.api_client_factory.override(providers.Factory(ApiClientStub))
    service1 = container.service_factory()
    assert isinstance(service1.api_client, ApiClientStub)

    # 2. Use .override() as a context manager to mock the API client in testing
    with container.api_client_factory.override(unittest.mock.Mock(ApiClient)):
        service2 = container.service_factory()
        assert isinstance(service2.api_client, unittest.mock.Mock)

    # 3. Use .reset_override() to get back to normal
    container.api_client_factory.reset_override()
    service3 = container.service_factory()
    assert isinstance(service3.api_client, ApiClient)
