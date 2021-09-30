"""`Factory` specialization with limitation to provided type example."""

from dependency_injector import containers, providers, errors


class BaseService:
    ...


class SomeService(BaseService):
    ...


class ServiceProvider(providers.Factory):

    provided_type = BaseService


# Creating service provider with a correct provided type:
class Services(containers.DeclarativeContainer):

    some_service_provider = ServiceProvider(SomeService)


# Trying to create service provider an incorrect provided type:
try:
    class Container(containers.DeclarativeContainer):
        some_service_provider = ServiceProvider(object)
except errors.Error as exception:
    print(exception)
    # The output is:
    # <class "__main__.ServiceProvider"> can provide only
    # <class "__main__.BaseService"> instances
