"""`Configuration` provider strict mode example."""

from dependency_injector import containers, providers, errors


class ApiClient:
    def __init__(self, api_key: str, timeout: int):
        self.api_key = api_key
        self.timeout = timeout


class Container(containers.DeclarativeContainer):

    config = providers.Configuration(strict=True)

    api_client_factory = providers.Factory(
        ApiClient,
        api_key=config.api.key,
        timeout=config.api.timeout.as_int(),
    )


if __name__ == "__main__":
    container = Container()

    try:
        api_client = container.api_client_factory()
    except errors.Error:
        # raises error: Undefined configuration option "config.api.key"
        ...
