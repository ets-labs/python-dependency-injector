"""Catalogs module."""

import six

from .errors import Error
from .errors import UndefinedProviderError

from .utils import is_provider
from .utils import is_catalog
from .utils import ensure_is_provider
from .utils import ensure_is_catalog_bundle


@six.python_2_unicode_compatible
class CatalogBundle(object):
    """Bundle of catalog providers."""

    catalog = None
    """:type: DeclarativeCatalog"""

    __IS_CATALOG_BUNDLE__ = True
    __slots__ = ('providers', '__dict__')

    def __init__(self, *providers):
        """Initializer."""
        self.providers = dict()
        for provider in providers:
            provider_name = self.catalog.get_provider_bind_name(provider)
            self.providers[provider_name] = provider
        self.__dict__.update(self.providers)
        super(CatalogBundle, self).__init__()

    @classmethod
    def sub_cls_factory(cls, catalog):
        """Create bundle class for catalog.

        :rtype: CatalogBundle
        :return: Subclass of CatalogBundle
        """
        return type('BundleSubclass', (cls,), dict(catalog=catalog))

    def get_provider(self, name):
        """Return provider with specified name or raise an error."""
        try:
            return self.providers[name]
        except KeyError:
            raise Error('Provider "{0}" is not a part of {1}'.format(name,
                                                                     self))

    def has_provider(self, name):
        """Check if there is provider with certain name."""
        return name in self.providers

    def __getattr__(self, item):
        """Raise an error on every attempt to get undefined provider."""
        if item.startswith('__') and item.endswith('__'):
            return super(CatalogBundle, self).__getattr__(item)
        raise UndefinedProviderError('Provider "{0}" is not a part '
                                     'of {1}'.format(item, self))

    def __repr__(self):
        """Return string representation of catalog bundle."""
        return '<{0}.Bundle({1})>'.format(
            self.catalog.name, ', '.join(six.iterkeys(self.providers)))

    __str__ = __repr__


@six.python_2_unicode_compatible
class DynamicCatalog(object):
    """Catalog of providers."""

    __IS_CATALOG__ = True
    __slots__ = ('name', 'providers', 'provider_names', 'overridden_by',
                 'Bundle')

    def __init__(self, **providers):
        """Initializer.

        :type providers: dict[str, dependency_injector.providers.Provider]
        """
        self.name = '.'.join((self.__class__.__module__,
                              self.__class__.__name__))
        self.providers = dict()
        self.provider_names = dict()
        self.overridden_by = tuple()

        self.Bundle = CatalogBundle.sub_cls_factory(self)
        """Catalog's bundle class.

        :type: :py:class:`dependency_injector.catalogs.CatalogBundle`
        """

        self.bind_providers(providers)
        super(DynamicCatalog, self).__init__()

    def is_bundle_owner(self, bundle):
        """Check if catalog is bundle owner."""
        return ensure_is_catalog_bundle(bundle) and bundle.catalog is self

    def get_provider_bind_name(self, provider):
        """Return provider's name in catalog."""
        if not self.is_provider_bound(provider):
            raise Error('Can not find bind name for {0} in catalog {1}'.format(
                provider, self))
        return self.provider_names[provider]

    def is_provider_bound(self, provider):
        """Check if provider is bound to the catalog."""
        return provider in self.provider_names

    def filter(self, provider_type):
        """Return dict of providers, that are instance of provided type."""
        return dict((name, provider)
                    for name, provider in six.iteritems(self.providers)
                    if isinstance(provider, provider_type))

    @property
    def is_overridden(self):
        """Check if catalog is overridden by another catalog."""
        return bool(self.overridden_by)

    @property
    def last_overriding(self):
        """Return last overriding catalog."""
        try:
            return self.overridden_by[-1]
        except (TypeError, IndexError):
            raise Error('Catalog {0} is not overridden'.format(self))

    def override(self, overriding):
        """Override current catalog providers by overriding catalog providers.

        :type overriding: DynamicCatalog
        """
        self.overridden_by += (overriding,)
        for name, provider in six.iteritems(overriding.providers):
            self.get_provider(name).override(provider)

    def reset_last_overriding(self):
        """Reset last overriding catalog."""
        if not self.is_overridden:
            raise Error('Catalog {0} is not overridden'.format(self))
        self.overridden_by = self.overridden_by[:-1]
        for provider in six.itervalues(self.providers):
            provider.reset_last_overriding()

    def reset_override(self):
        """Reset all overridings for all catalog providers."""
        self.overridden_by = tuple()
        for provider in six.itervalues(self.providers):
            provider.reset_override()

    def get_provider(self, name):
        """Return provider with specified name or raise an error."""
        try:
            return self.providers[name]
        except KeyError:
            raise UndefinedProviderError('{0} has no provider with such '
                                         'name - {1}'.format(self, name))

    def bind_provider(self, name, provider):
        """Bind provider to catalog with specified name."""
        provider = ensure_is_provider(provider)

        if name in self.providers:
            raise Error('Catalog {0} already has provider with '
                        'such name - {1}'.format(self, name))
        if provider in self.provider_names:
            raise Error('Catalog {0} already has such provider '
                        'instance - {1}'.format(self, provider))

        self.providers[name] = provider
        self.provider_names[provider] = name

    def bind_providers(self, providers):
        """Bind providers dictionary to catalog."""
        for name, provider in six.iteritems(providers):
            self.bind_provider(name, provider)

    def has_provider(self, name):
        """Check if there is provider with certain name."""
        return name in self.providers

    def unbind_provider(self, name):
        """Remove provider binding."""
        provider = self.get_provider(name)
        del self.providers[name]
        del self.provider_names[provider]

    def __getattr__(self, name):
        """Return provider with specified name or raise en error."""
        return self.get_provider(name)

    def __setattr__(self, name, value):
        """Handle setting of catalog attributes.

        Setting of attributes works as usual, but if value of attribute is
        provider, this provider will be bound to catalog correctly.
        """
        if is_provider(value):
            return self.bind_provider(name, value)
        return super(DynamicCatalog, self).__setattr__(name, value)

    def __delattr__(self, name):
        """Handle deleting of catalog attibute.

        Deleting of attributes works as usual, but if value of attribute is
        provider, this provider will be unbound from catalog correctly.
        """
        self.unbind_provider(name)

    def __repr__(self):
        """Return Python representation of catalog."""
        return '<{0}({1})>'.format(self.name,
                                   ', '.join(six.iterkeys(self.providers)))

    __str__ = __repr__


@six.python_2_unicode_compatible
class DeclarativeCatalogMetaClass(type):
    """Declarative catalog meta class."""

    def __new__(mcs, class_name, bases, attributes):
        """Declarative catalog class factory."""
        cls_providers = tuple((name, provider)
                              for name, provider in six.iteritems(attributes)
                              if is_provider(provider))

        inherited_providers = tuple((name, provider)
                                    for base in bases if is_catalog(base)
                                    for name, provider in six.iteritems(
                                        base.providers))

        providers = cls_providers + inherited_providers

        cls = type.__new__(mcs, class_name, bases, attributes)

        cls._catalog = DynamicCatalog()
        cls._catalog.name = '.'.join((cls.__module__, cls.__name__))
        cls._catalog.bind_providers(dict(providers))

        cls.cls_providers = dict(cls_providers)
        cls.inherited_providers = dict(inherited_providers)

        cls.Bundle = cls._catalog.Bundle

        return cls

    @property
    def name(cls):
        """Read-only property that represents catalog's name.

        Catalog's name is catalog's module + catalog's class name.

        :type: str
        """
        return cls._catalog.name

    @property
    def providers(cls):
        """Read-only dictionary of all providers.

        :type: dict[str, :py:class:`dependency_injector.providers.Provider`]
        """
        return cls._catalog.providers

    @property
    def overridden_by(cls):
        """Tuple of overriding catalogs.

        :type: tuple[
            :py:class:`dependency_injector.catalogs.DeclarativeCatalog` |
            :py:class:`dependency_injector.catalogs.DynamicCatalog`]
        """
        return cls._catalog.overridden_by

    @property
    def is_overridden(cls):
        """Check if catalog is overridden by another catalog.

        :rtype: bool
        """
        return cls._catalog.is_overridden

    @property
    def last_overriding(cls):
        """Read-only reference to the last overriding catalog, if any.

        :type: :py:class:`dependency_injector.catalogs.DeclarativeCatalog` |
            :py:class:`dependency_injector.catalogs.DynamicCatalog`
        """
        return cls._catalog.last_overriding

    def __getattr__(cls, name):
        """Return provider with specified name or raise en error.

        :param name: Attribute's name
        :type name: str

        :raise: :py:class:`dependency_injector.errors.UndefinedProviderError`
        """
        raise UndefinedProviderError('There is no provider "{0}" in '
                                     'catalog {1}'.format(name, cls))

    def __setattr__(cls, name, value):
        """Handle setting of catalog attributes.

        Setting of attributes works as usual, but if value of attribute is
        provider, this provider will be bound to catalog.

        :param name: Attribute's name
        :type name: str

        :param value: Attribute's value
        :type value: :py:class:`dependency_injector.providers.Provider` |
                     object

        :rtype: None
        """
        if is_provider(value):
            setattr(cls._catalog, name, value)
        return super(DeclarativeCatalogMetaClass, cls).__setattr__(name, value)

    def __delattr__(cls, name):
        """Handle deleting of catalog attibute.

        Deleting of attributes works as usual, but if value of attribute is
        provider, this provider will be unbound from catalog.

        :param name: Attribute's name
        :type name: str

        :rtype: None
        """
        if is_provider(getattr(cls, name)):
            delattr(cls._catalog, name)
        return super(DeclarativeCatalogMetaClass, cls).__delattr__(name)

    def __repr__(cls):
        """Return string representation of the catalog.

        :rtype: str
        """
        return '<{0}({1})>'.format(cls.name,
                                   ', '.join(six.iterkeys(cls.providers)))

    __str__ = __repr__


@six.add_metaclass(DeclarativeCatalogMetaClass)
class DeclarativeCatalog(object):
    """Declarative catalog of providers.

    ``DeclarativeCatalog`` is a catalog of providers that could be defined in
    declarative manner. It should cover most of the cases when list of
    providers that would be included in catalog is deterministic (catalog will
    not change its structure in runtime).
    """

    Bundle = CatalogBundle
    """Catalog's bundle class.

    :type: :py:class:`dependency_injector.catalogs.CatalogBundle`
    """

    name = str()
    """Read-only property that represents catalog's name.

    Catalog's name is catalog's module + catalog's class name.

    :type: str
    """

    cls_providers = dict()
    """Read-only dictionary of current catalog providers.

    :type: dict[str, :py:class:`dependency_injector.providers.Provider`]
    """

    inherited_providers = dict()
    """Read-only dictionary of inherited providers.

    :type: dict[str, :py:class:`dependency_injector.providers.Provider`]
    """

    providers = dict()
    """Read-only dictionary of all providers.

    :type: dict[str, :py:class:`dependency_injector.providers.Provider`]
    """

    overridden_by = tuple()
    """Tuple of overriding catalogs.

    :type: tuple[:py:class:`dependency_injector.catalogs.DeclarativeCatalog` |
                 :py:class:`dependency_injector.catalogs.DynamicCatalog`]
    """

    is_overridden = bool
    """Read-only property that is set to True if catalog is overridden.

    :type: bool
    """

    last_overriding = None
    """Read-only reference to the last overriding catalog, if any.

    :type: :py:class:`dependency_injector.catalogs.DeclarativeCatalog` |
           :py:class:`dependency_injector.catalogs.DynamicCatalog`
    """

    _catalog = DynamicCatalog

    __IS_CATALOG__ = True

    @classmethod
    def is_bundle_owner(cls, bundle):
        """Check if catalog is bundle owner.

        :param bundle: Catalog's bundle instance
        :type bundle: :py:class:`dependency_injector.catalogs.CatalogBundle`

        :rtype: bool
        """
        return cls._catalog.is_bundle_owner(bundle)

    @classmethod
    def get_provider_bind_name(cls, provider):
        """Return provider's name in catalog.

        :param provider: Provider instance
        :type provider: :py:class:`dependency_injector.providers.Provider`

        :raise: :py:class:`dependency_injector.errors.UndefinedProviderError`

        :return: Provider's name
        :rtype: str
        """
        return cls._catalog.get_provider_bind_name(provider)

    @classmethod
    def is_provider_bound(cls, provider):
        """Check if provider is bound to the catalog.

        :param provider: Provider instance
        :type provider: :py:class:`dependency_injector.providers.Provider`

        :rtype: bool
        """
        return cls._catalog.is_provider_bound(provider)

    @classmethod
    def filter(cls, provider_type):
        """Return dict of providers, that are instance of provided type.

        :param provider_type: Provider type
        :type provider: :py:class:`dependency_injector.providers.Provider`
        """
        return cls._catalog.filter(provider_type)

    @classmethod
    def override(cls, overriding):
        """Override current catalog providers by overriding catalog providers.

        :param overriding: Overriding catalog
        :type overriding:
            :py:class:`dependency_injector.catalogs.DeclarativeCatalog` |
            :py:class:`dependency_injector.catalogs.DynamicCatalog`

        :rtype: None
        """
        return cls._catalog.override(overriding)

    @classmethod
    def reset_last_overriding(cls):
        """Reset last overriding catalog.

        :rtype: None
        """
        cls._catalog.reset_last_overriding()

    @classmethod
    def reset_override(cls):
        """Reset all overridings for all catalog providers.

        :rtype: None
        """
        cls._catalog.reset_override()

    @classmethod
    def get_provider(cls, name):
        """Return provider with specified name or raise an error.

        :param name: Provider's name
        :type name: str

        :raise: :py:class:`dependency_injector.errors.UndefinedProviderError`

        :return: Provider with specified name
        :rtype: :py:class:`dependency_injector.providers.Provider`
        """
        return cls._catalog.get_provider(name)

    get = get_provider  # Backward compatibility for versions < 0.11.*

    @classmethod
    def bind_provider(cls, name, provider):
        """Bind provider to catalog with specified name.

        :param name: Name of the provider
        :type name: str

        :param provider: Provider instance
        :type provider: :py:class:`dependency_injector.providers.Provider`

        :raise: :py:class:`dependency_injector.errors.Error`

        :rtype: None
        """
        setattr(cls, name, provider)

    @classmethod
    def bind_providers(cls, providers):
        """Bind providers dictionary to catalog.

        :param providers: Dictionary of providers, where key is a name
            and value is a provider
        :type providers:
            dict[str, :py:class:`dependency_injector.providers.Provider`]

        :raise: :py:class:`dependency_injector.errors.Error`

        :rtype: None
        """
        for name, provider in six.iteritems(providers):
            setattr(cls, name, provider)

    @classmethod
    def has_provider(cls, name):
        """Check if there is provider with certain name.

        :param name: Provider's name
        :type name: str

        :rtype: bool
        """
        return hasattr(cls, name)

    has = has_provider  # Backward compatibility for versions < 0.11.*

    @classmethod
    def unbind_provider(cls, name):
        """Remove provider binding.

        :param name: Provider's name
        :type name: str

        :rtype: None
        """
        delattr(cls, name)

    @classmethod
    def __getattr__(cls, name):
        """Return provider with specified name or raise en error.

        :param name: Attribute's name
        :type name: str

        :raise: :py:class:`dependency_injector.errors.UndefinedProviderError`
        """
        raise NotImplementedError('Implementated in metaclass')

    @classmethod
    def __setattr__(cls, name, value):
        """Handle setting of catalog attributes.

        Setting of attributes works as usual, but if value of attribute is
        provider, this provider will be bound to catalog.

        :param name: Attribute's name
        :type name: str

        :param value: Attribute's value
        :type value: :py:class:`dependency_injector.providers.Provider` |
                     object

        :rtype: None
        """
        raise NotImplementedError('Implementated in metaclass')

    @classmethod
    def __delattr__(cls, name):
        """Handle deleting of catalog attibute.

        Deleting of attributes works as usual, but if value of attribute is
        provider, this provider will be unbound from catalog.

        :param name: Attribute's name
        :type name: str

        :rtype: None
        """
        raise NotImplementedError('Implementated in metaclass')


# Backward compatibility for versions < 0.11.*
AbstractCatalog = DeclarativeCatalog


def override(catalog):
    """Catalog overriding decorator.

    :param catalog: Catalog that should be overridden by decorated catalog.
    :type catalog: :py:class:`dependency_injector.catalogs.DeclarativeCatalog`

    :return: Declarative catalog's overriding decorator
    :rtype: callable(
        :py:class:`dependency_injector.catalogs.DeclarativeCatalog`)
    """
    def decorator(overriding_catalog):
        """Overriding decorator."""
        catalog.override(overriding_catalog)
        return overriding_catalog
    return decorator
