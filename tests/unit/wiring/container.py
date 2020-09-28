from dependency_injector import containers, providers

from .service import Service


class SubContainer(containers.DeclarativeContainer):

    int_object = providers.Object(1)


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()

    service = providers.Factory(Service)

    sub = providers.Container(SubContainer)
