from dependency_injector import containers, providers

from .service import Service


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()

    service = providers.Factory(Service)
