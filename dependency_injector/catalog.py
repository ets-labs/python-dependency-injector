"""Catalog module."""

import six

from .errors import Error

from .utils import is_provider
from .utils import is_catalog


class CatalogPackFactory(object):
    """Factory of catalog packs."""

    def __init__(self, catalog):
        """Initializer."""
        self.catalog = catalog

    def __call__(self, *providers):
        """Create catalog pack with specified providers."""
        return CatalogPack(self.catalog, *providers)


class CatalogPack(object):
    """Pack of catalog providers."""

    __slots__ = ('catalog', 'providers', '__dict__')

    def __init__(self, catalog, *providers):
        """Initializer."""
        self.catalog = catalog
        self.providers = dict()
        for provider in providers:
            self._ensure_provider_is_bound(provider)
            self.__dict__[provider.bind.name] = provider
            self.providers[provider.bind.name] = provider
        super(CatalogPack, self).__init__()

    def get(self, name):
        """Return provider with specified name or raises error."""
        try:
            return self.providers[name]
        except KeyError:
            self._raise_undefined_provider_error(name)

    def has(self, name):
        """Check if there is provider with certain name."""
        return name in self.providers

    def _ensure_provider_is_bound(self, provider):
        """Check that provider is bound."""
        if not provider.bind:
            raise Error('Provider {0} is not bound to '
                        'any catalog'.format(provider))
        if provider is not self.catalog.get(provider.bind.name):
            raise Error('{0} can contain providers from '
                        'catalog {0}' .format(self, self.catalog))

    def _raise_undefined_provider_error(self, name):
        """Raise error for cases when there is no such provider in pack."""
        raise Error('Provider "{0}" is not a part of {1}'.format(name, self))

    def __getattr__(self, item):
        """Raise an error on every attempt to get undefined provider."""
        self._raise_undefined_provider_error(item)

    def __repr__(self):
        """Return string representation of pack."""
        return '<Catalog pack ({0}), {1}>'.format(
            ', '.join(six.iterkeys(self.providers)), self.catalog)


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

        cls = type.__new__(mcs, class_name, bases, attributes)

        cls.cls_providers = cls_providers
        cls.inherited_providers = inherited_providers
        cls.providers = providers

        cls.Pack = CatalogPackFactory(cls)

        for name, provider in six.iteritems(cls_providers):
            provider.bind = ProviderBinding(cls, name)

        return cls

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

    :type Pack: CatalogPack
    :param Pack: Catalog's pack class
    """

    Pack = CatalogPackFactory

    cls_providers = dict()
    inherited_providers = dict()
    providers = dict()

    __IS_CATALOG__ = True

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


class ProviderBinding(object):
    """Catalog provider binding."""

    __slots__ = ('catalog', 'name')

    def __init__(self, catalog, name):
        """Initializer."""
        self.catalog = catalog
        self.name = name


def override(catalog):
    """Catalog overriding decorator."""
    def decorator(overriding_catalog):
        """Overriding decorator."""
        catalog.override(overriding_catalog)
        return overriding_catalog
    return decorator
