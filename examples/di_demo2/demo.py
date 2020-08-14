from dependency_injector import containers, providers
from unittest import mock

from .example_di import ApiClient, Service


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()

    api_client = providers.Singleton(
        ApiClient,
        api_key=config.api_key,
        timeout=config.timeout,
    )

    service = providers.Factory(
        Service,
        api_client=api_client,
    )


if __name__ == '__main__':
    container = Container()
    container.config.from_yaml('config.yml')

    service = container.service()
    assert isinstance(service.api_client, ApiClient)

    with container.api_client.override(mock.Mock()):
        service = container.service()
        assert isinstance(service.api_client, mock.Mock)
