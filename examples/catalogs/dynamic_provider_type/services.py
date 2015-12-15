"""Base classes for services."""

from dependency_injector import catalogs
from dependency_injector import providers


class Base(object):
    """Base service class."""


class Provider(providers.Factory):
    """Service provider.

    Can provide :py:class:`Base` only.
    """

    provided_type = Base


class Catalog(catalogs.DynamicCatalog):
    """Base catalog of services.

    Can include :py:class:`Provider`'s only.
    """

    provider_type = Provider
