"""The Code, that uses IoC container."""

from dependency_injector import catalogs
from dependency_injector import providers

from ioc_example import Service
from ioc_example import Client


class Components(catalogs.DeclarativeCatalog):
    """Catalog of component providers."""

    service = providers.Factory(Service)

    client = providers.Factory(Client, service=service)


if __name__ == '__main__':
    client = Components.client()  # Application creates Client's instance
