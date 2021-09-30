"""`Factory` provider attribute injections example."""

from dependency_injector import containers, providers


class Client:
    ...


class Service:
    def __init__(self) -> None:
        self.client = None


class Container(containers.DeclarativeContainer):

    client = providers.Factory(Client)

    service = providers.Factory(Service)
    service.add_attributes(client=client)


if __name__ == "__main__":
    container = Container()

    service = container.service()

    assert isinstance(service.client, Client)
