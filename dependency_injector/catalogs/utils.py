"""Dependency injector catalog utils."""

import six

from dependency_injector.utils import _copy_providers
from dependency_injector.errors import UndefinedProviderError


def copy(catalog):
    """:py:class:`DeclarativeCatalog` copying decorator.

    This decorator copy all providers from provided catalog to decorated one.
    If one of the decorated catalog providers matches to source catalog
    providers by name, it would be replaced by reference.

    :param catalog: Catalog that should be copied by decorated catalog.
    :type catalog: :py:class:`DeclarativeCatalog`

    :return: Declarative catalog's copying decorator.
    :rtype:
        callable(:py:class:`DeclarativeCatalog`)
    """
    def decorator(copied_catalog):
        """Copying decorator.

        :param copied_catalog: Decorated catalog.
        :type copied_catalog: :py:class:`DeclarativeCatalog`

        :return: Decorated catalog.
        :rtype:
            :py:class:`DeclarativeCatalog`
        """
        memo = dict()
        for name, provider in six.iteritems(copied_catalog.cls_providers):
            try:
                source_provider = catalog.get_provider(name)
            except UndefinedProviderError:
                pass
            else:
                memo[id(source_provider)] = provider

        copied_catalog.bind_providers(_copy_providers(catalog.providers, memo),
                                      force=True)

        return copied_catalog
    return decorator


def override(catalog):
    """:py:class:`DeclarativeCatalog` overriding decorator.

    :param catalog: Catalog that should be overridden by decorated catalog.
    :type catalog: :py:class:`DeclarativeCatalog`

    :return: Declarative catalog's overriding decorator.
    :rtype: callable(:py:class:`DeclarativeCatalog`)
    """
    def decorator(overriding_catalog):
        """Overriding decorator."""
        catalog.override(overriding_catalog)
        return overriding_catalog
    return decorator
