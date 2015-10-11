"""Catalog module."""

import six

from .errors import Error

from .utils import is_provider
from .utils import is_catalog


class CatalogMetaClass(type):
    """Providers catalog meta class."""

    def __new__(mcs, class_name, bases, attributes):
        """Meta class factory."""
        cls_providers = dict((name, provider)
                             for name, provider in six.iteritems(attributes)
                             if is_provider(provider))

        inherited_providers = dict((name, provider)
                                   for base in bases if is_catalog(base)
                                   for name, provider in six.iteritems(
                                       base.providers))

        providers = dict()
        providers.update(cls_providers)
        providers.update(inherited_providers)

        attributes['cls_providers'] = cls_providers
        attributes['inherited_providers'] = inherited_providers
        attributes['providers'] = providers
        return type.__new__(mcs, class_name, bases, attributes)


@six.add_metaclass(CatalogMetaClass)
class AbstractCatalog(object):
    """Abstract providers catalog.

    :type providers: dict[str, dependency_injector.Provider]
    :param providers: Dict of all catalog providers, including inherited from
        parent catalogs

    :type cls_providers: dict[str, dependency_injector.Provider]
    :param cls_providers: Dict of current catalog providers

    :type inherited_providers: dict[str, dependency_injector.Provider]
    :param inherited_providers: Dict of providers, that are inherited from
        parent catalogs
    """

    providers = dict()
    cls_providers = dict()
    inherited_providers = dict()

    __IS_CATALOG__ = True
    __slots__ = ('used_providers',)

    def __init__(self, *used_providers):
        """Initializer."""
        self.used_providers = set(used_providers)

    def __getattribute__(self, item):
        """Return providers."""
        attribute = super(AbstractCatalog, self).__getattribute__(item)
        if item in ('providers', 'used_providers', '__class__'):
            return attribute

        if attribute not in self.used_providers:
            raise Error('Provider \'{0}\' '.format(item) +
                        'is not listed in dependencies')
        return attribute

    @classmethod
    def filter(cls, provider_type):
        """Return dict of providers, that are instance of provided type."""
        return dict((name, provider)
                    for name, provider in six.iteritems(cls.providers)
                    if isinstance(provider, provider_type))

    @classmethod
    def override(cls, overriding):
        """Override current catalog providers by overriding catalog providers.

        :type overriding: AbstractCatalog
        """
        for name, provider in six.iteritems(overriding.cls_providers):
            cls.providers[name].override(provider)


def override(catalog):
    """Catalog overriding decorator."""
    def decorator(overriding_catalog):
        """Overriding decorator."""
        catalog.override(overriding_catalog)
        return overriding_catalog
    return decorator
