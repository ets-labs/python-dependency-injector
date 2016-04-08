"""Dependency injector catalog utils."""

import six

from copy import deepcopy


def copy(catalog):
    """:py:class:`DeclarativeCatalog` copying decorator.

    :param catalog: Catalog that should be copied by decorated catalog.
    :type catalog: :py:class:`dependency_injector.catalogs.DeclarativeCatalog`
                 | :py:class:`dependency_injector.catalogs.DynamicCatalog`

    :return: Declarative catalog's copying decorator.
    :rtype:
        callable(:py:class:`dependency_injector.catalogs.DeclarativeCatalog`)
    """
    def decorator(overriding_catalog):
        """Overriding decorator.

        :param catalog: Decorated catalog.
        :type catalog:
            :py:class:`dependency_injector.catalogs.DeclarativeCatalog`

        :return: Decorated catalog.
        :rtype:
            :py:class:`dependency_injector.catalogs.DeclarativeCatalog`
        """
        memo = dict()

        for name, provider in six.iteritems(overriding_catalog.providers):
            memo[id(catalog.get_provider(name))] = provider

        dynamic_catalog_copy = deepcopy(catalog._catalog, memo)

        print dynamic_catalog_copy.providers

        for name, provider in six.iteritems(dynamic_catalog_copy.providers):
            overriding_catalog.bind_provider(name, provider)

        return overriding_catalog
    return decorator


def override(catalog):
    """:py:class:`DeclarativeCatalog` overriding decorator.

    :param catalog: Catalog that should be overridden by decorated catalog.
    :type catalog: :py:class:`DeclarativeCatalog` | :py:class:`DynamicCatalog`

    :return: Declarative catalog's overriding decorator.
    :rtype: callable(:py:class:`DeclarativeCatalog`)
    """
    def decorator(overriding_catalog):
        """Overriding decorator."""
        catalog.override(overriding_catalog)
        return overriding_catalog
    return decorator
