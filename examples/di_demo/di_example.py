"""The Code, powered by Dependency Injector."""

from dependency_injector import catalogs, providers
from ioc_example import Service, Client


class Components(catalogs.DeclarativeCatalog):
    """Components catalog."""

    service = providers.Factory(Service)
    """:type: providers.Factory -> Service"""

    client = providers.Factory(Client,
                               service=service)
    """:type: providers.Factory -> Client"""


if __name__ == '__main__':
    # Application creates Client's instance using its provider
    client = Components.client()  # equivalent of Client(service=Service())
