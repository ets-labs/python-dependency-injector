from dependency_injector import containers, providers


class ApiClient:

    def __init__(self, api_key: str, timeout: int):
        self.api_key = api_key
        self.timeout = timeout


class Service:

    def __init__(self, api_client: ApiClient):
        self.api_client = api_client


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
