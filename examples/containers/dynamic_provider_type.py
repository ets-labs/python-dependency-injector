"""Dynamic container provider type restriction example."""

import abc

from dependency_injector import containers, providers


class Service(metaclass=abc.ABCMeta):
    ...


class UserService(Service):
    ...


class ServiceProvider(providers.Factory):

    provided_type = Service


services = containers.DynamicContainer()
services.provider_type = ServiceProvider

services.user_service = ServiceProvider(UserService)
services.other_provider = providers.Factory(object)
