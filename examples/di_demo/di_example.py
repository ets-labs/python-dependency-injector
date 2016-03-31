"""The Code, powered by Dependency Injector."""

from dependency_injector import catalogs, providers
from ioc_example import Service, Client


class Components(catalogs.DeclarativeCatalog):
    """Components catalog."""

    service = providers.Factory(Service)
    client = providers.Factory(Client, service=service)


if __name__ == '__main__':
    client = Components.client()  # Application creates Client's instance
