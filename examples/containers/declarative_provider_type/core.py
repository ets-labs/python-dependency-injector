"""Base classes for services."""

from dependency_injector import containers
from dependency_injector import providers


class BaseService(object):
    """Base service class."""


class ServiceProvider(providers.Factory):
    """Service provider.

    Can provide :py:class:`Base` only.
    """

    provided_type = BaseService


class ServicesContainer(containers.DeclarativeContainer):
    """Base IoC container of service providers.

    Can include :py:class:`Provider`'s only.
    """

    provider_type = ServiceProvider
