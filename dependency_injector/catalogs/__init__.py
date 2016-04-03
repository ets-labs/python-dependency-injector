"""Dependency injector catalogs package."""

from dependency_injector.catalogs.bundle import CatalogBundle

from dependency_injector.catalogs.dynamic import DynamicCatalog

from dependency_injector.catalogs.declarative import (
    DeclarativeCatalogMetaClass,
    DeclarativeCatalog,
    AbstractCatalog,
)


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


__all__ = (
    'CatalogBundle',
    'DynamicCatalog',
    'DeclarativeCatalogMetaClass',
    'DeclarativeCatalog',
    'AbstractCatalog',
    'override',
)
