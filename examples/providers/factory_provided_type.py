"""`Factory` specialization with limitation to provided type example."""

import dependency_injector.providers as providers
import dependency_injector.errors as errors


class BaseService:
    """Base service class."""


class SomeService(BaseService):
    """Some service."""


class ServiceProvider(providers.Factory):
    """Service provider."""

    provided_type = BaseService


# Creating service provider with correct provided type:
some_service_provider = ServiceProvider(SomeService)

# Trying to create service provider incorrect provided type:
try:
    some_service_provider = ServiceProvider(object)
except errors.Error as exception:
    print(exception)
    # <class '__main__.ServiceProvider'> can provide only
    # <class '__main__.BaseService'> instances
