"""Catalog module."""

import six

from .errors import Error

from .utils import is_provider
from .utils import is_catalog
from .utils import ensure_is_catalog_bundle


class CatalogBundle(object):
    """Bundle of catalog providers."""

    catalog = None
    """:type: AbstractCatalog"""

    __IS_CATALOG_BUNDLE__ = True
    __slots__ = ('providers', '__dict__')

    def __init__(self, *providers):
        """Initializer."""
        self.providers = dict((provider.bind.name, provider)
                              for provider in providers
                              if self._ensure_provider_is_bound(provider))
        self.__dict__.update(self.providers)
        super(CatalogBundle, self).__init__()

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
        """Check that provider is bound to the bundle's catalog."""
        if not provider.is_bound:
            raise Error('Provider {0} is not bound to '
                        'any catalog'.format(provider))
        if provider is not self.catalog.get(provider.bind.name):
            raise Error('{0} can contain providers from '
                        'catalog {0}'.format(self.__class__, self.catalog))
        return True

    def _raise_undefined_provider_error(self, name):
        """Raise error for cases when there is no such provider in bundle."""
        raise Error('Provider "{0}" is not a part of {1}'.format(name, self))

    def __getattr__(self, item):
        """Raise an error on every attempt to get undefined provider."""
        if item.startswith('__') and item.endswith('__'):
            return super(CatalogBundle, self).__getattr__(item)
        self._raise_undefined_provider_error(item)

    def __repr__(self):
        """Return string representation of bundle."""
        return '<Bundle of {0} providers ({1})>'.format(
            self.catalog, ', '.join(six.iterkeys(self.providers)))


class CatalogMetaClass(type):
    """Catalog meta class."""

    def __new__(mcs, class_name, bases, attributes):
        """Catalog class factory."""
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

        cls.Bundle = mcs.bundle_cls_factory(cls)

        for name, provider in six.iteritems(cls_providers):
            if provider.is_bound:
                raise Error('Provider {0} has been already bound to catalog'
                            '{1} as "{2}"'.format(provider,
                                                  provider.bind.catalog,
                                                  provider.bind.name))
            provider.bind = ProviderBinding(cls, name)

        return cls

    @classmethod
    def bundle_cls_factory(mcs, cls):
        """Create bundle class for catalog."""
        return type('{0}Bundle', (CatalogBundle,), dict(catalog=cls))

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

    :type Bundle: CatalogBundle
    :param Bundle: Catalog's bundle class
    """

    Bundle = CatalogBundle

    cls_providers = dict()
    inherited_providers = dict()
    providers = dict()

    __IS_CATALOG__ = True

    @classmethod
    def is_bundle_owner(cls, bundle):
        """Check if catalog is bundle owner."""
        return ensure_is_catalog_bundle(bundle) and bundle.catalog is cls

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
