"""Declarative container provider type restriction example."""

import abc

from dependency_injector import containers, providers


class Service(metaclass=abc.ABCMeta):
    ...


class UserService(Service):
    ...


class ServiceProvider(providers.Factory):

    provided_type = Service


class ServiceContainer(containers.DeclarativeContainer):

    provider_type = ServiceProvider


class MyServices(ServiceContainer):

    user_service = ServiceProvider(UserService)


class ImproperServices(ServiceContainer):

    other_provider = providers.Factory(object)
