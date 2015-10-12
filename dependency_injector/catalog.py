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

    def __repr__(cls):
        """Return string representation of the catalog class."""
        return '<Catalog "' + '.'.join((cls.__module__, cls.__name__)) + '">'


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

    def __new__(cls, *providers):
        """Catalog constructor.

        Catalogs are declaratives entities that could not be instantiated.
        Catalog constructor is designed to produce subsets of catalog
        providers.
        """
        return CatalogSubset(catalog=cls, providers=providers)

    @classmethod
    def is_subset_owner(cls, subset):
        """Check if catalog is subset owner."""
        return subset.catalog is cls

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

    @classmethod
    def get(cls, name):
        """Return provider with specified name or raises error."""
        try:
            return cls.providers[name]
        except KeyError:
            raise Error('{0} has no provider with such name - {1}'.format(
                cls, name))

    @classmethod
    def has(cls, name):
        """Check if there is provider with certain name."""
        return name in cls.providers


class CatalogSubset(object):
    """Subset of catalog providers."""

    __IS_SUBSET__ = True
    __slots__ = ('catalog', 'available_providers', 'providers', '__dict__')

    def __init__(self, catalog, providers):
        """Initializer."""
        self.catalog = catalog
        self.available_providers = set(providers)
        self.providers = dict()
        for provider_name in self.available_providers:
            try:
                provider = self.catalog.providers[provider_name]
            except KeyError:
                raise Error('Subset could not add "{0}" provider in scope, '
                            'because {1} has no provider with '
                            'such name'.format(provider_name, self.catalog))
            else:
                self.providers[provider_name] = provider
        self.__dict__.update(self.providers)
        super(CatalogSubset, self).__init__()

    def get(self, name):
        """Return provider with specified name or raises error."""
        try:
            return self.providers[name]
        except KeyError:
            self._raise_undefined_provider_error(name)

    def has(self, name):
        """Check if there is provider with certain name."""
        return name in self.providers

    def __getattr__(self, item):
        """Raise an error on every attempt to get undefined provider."""
        self._raise_undefined_provider_error(item)

    def __repr__(self):
        """Return string representation of subset."""
        return '<Subset ({0}), {1}>'.format(
            ', '.join(self.available_providers), self.catalog)

    def _raise_undefined_provider_error(self, name):
        """Raise error for cases when there is no such provider in subset."""
        raise Error('Provider "{0}" is not a part of {1}'.format(name, self))


def override(catalog):
    """Catalog overriding decorator."""
    def decorator(overriding_catalog):
        """Overriding decorator."""
        catalog.override(overriding_catalog)
        return overriding_catalog
    return decorator
