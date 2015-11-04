"""Catalog module."""

import six

from .errors import Error

from .utils import is_provider
from .utils import is_catalog
from .utils import ensure_is_catalog_bundle


@six.python_2_unicode_compatible
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
        """Return string representation of catalog bundle."""
        return '<{0}.{1}.Bundle({2})>'.format(
            self.catalog.__module__, self.catalog.__name__,
            ', '.join(six.iterkeys(self.providers)))

    __str__ = __repr__


@six.python_2_unicode_compatible
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

        cls.overridden_by = tuple()

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

    @property
    def is_overridden(cls):
        """Check if catalog is overridden by another catalog."""
        return bool(cls.overridden_by)

    @property
    def last_overriding(cls):
        """Return last overriding catalog."""
        try:
            return cls.overridden_by[-1]
        except (TypeError, IndexError):
            raise Error('Catalog {0} is not overridden'.format(str(cls)))

    def __repr__(cls):
        """Return string representation of the catalog class."""
        return '<{0}.{1}>'.format(cls.__module__, cls.__name__)

    __str__ = __repr__


@six.add_metaclass(CatalogMetaClass)
class AbstractCatalog(object):
    """Abstract providers catalog.

    :type Bundle: CatalogBundle
    :param Bundle: Catalog's bundle class

    :type providers: dict[str, dependency_injector.Provider]
    :param providers: Dict of all catalog providers, including inherited from
        parent catalogs

    :type cls_providers: dict[str, dependency_injector.Provider]
    :param cls_providers: Dict of current catalog providers

    :type inherited_providers: dict[str, dependency_injector.Provider]
    :param inherited_providers: Dict of providers, that are inherited from
        parent catalogs

    :type overridden_by: tuple[AbstractCatalog]
    :param overridden_by: Tuple of overriding catalogs

    :type is_overridden: bool
    :param is_overridden: Read-only, evaluated in runtime, property that is
        set to True if catalog is overridden

    :type last_overriding: AbstractCatalog | None
    :param last_overriding: Reference to the last overriding catalog, if any
    """

    Bundle = CatalogBundle

    cls_providers = dict()
    inherited_providers = dict()
    providers = dict()

    overridden_by = tuple()
    is_overridden = bool
    last_overriding = None

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
        cls.overridden_by += (overriding,)
        for name, provider in six.iteritems(overriding.cls_providers):
            cls.providers[name].override(provider)

    @classmethod
    def reset_last_overriding(cls):
        """Reset last overriding catalog."""
        if not cls.is_overridden:
            raise Error('Catalog {0} is not overridden'.format(str(cls)))
        cls.overridden_by = cls.overridden_by[:-1]
        for provider in six.itervalues(cls.providers):
            provider.reset_last_overriding()

    @classmethod
    def reset_override(cls):
        """Reset all overridings for all catalog providers."""
        cls.overridden_by = tuple()
        for provider in six.itervalues(cls.providers):
            provider.reset_override()

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
