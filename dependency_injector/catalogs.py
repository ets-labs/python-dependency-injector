"""Catalogs module."""

import six

from .errors import Error
from .errors import UndefinedProviderError

from .utils import is_provider
from .utils import is_catalog
from .utils import is_declarative_catalog
from .utils import ensure_is_provider
from .utils import ensure_is_catalog_bundle


@six.python_2_unicode_compatible
class CatalogBundle(object):
    """Bundle of catalog providers.

    :py:class:`CatalogBundle` is a frozen, limited collection of catalog
    providers. While catalog could be used as a centralized place for
    particular providers group, such bundles of catalog providers can be used
    for creating several frozen, limited scopes that could be passed to
    different subsystems.

    :py:class:`CatalogBundle` has API's parity with catalogs
    (:py:class:`DeclarativeCatalog` or :py:class:`DynamicCatalog`) in terms of
    retrieving the providers, but it is "frozen" in terms of modification
    provider's list.

    :py:class:`CatalogBundle` is considered to be dependable on catalogs
    (:py:class:`DeclarativeCatalog` or :py:class:`DynamicCatalog`) entity by
    its design.

    .. py:attribute:: catalog

        Bundle's catalog.

        :type: :py:class:`DeclarativeCatalog` | :py:class:`DynamicCatalog`

    .. py:attribute:: providers

        Dictionary of all providers.

        :type: dict[str, :py:class:`dependency_injector.providers.Provider`]
    """

    catalog = None

    __IS_CATALOG_BUNDLE__ = True
    __slots__ = ('providers', '__dict__')

    @classmethod
    def sub_cls_factory(cls, catalog):
        """Create bundle subclass for catalog.

        :return: Subclass of :py:class:`CatalogBundle`.
        :rtype: :py:class:`CatalogBundle`
        """
        return type('BundleSubclass', (cls,), dict(catalog=catalog))

    def __init__(self, *providers):
        """Initializer.

        :param providers: Tuple of catalog's bundle providers.
        :type providers: tuple[
            :py:class:`dependency_injector.providers.Provider`]
        """
        self.providers = dict((self.catalog.get_provider_bind_name(provider),
                               provider)
                              for provider in providers)
        self.__dict__.update(self.providers)
        super(CatalogBundle, self).__init__()

    def get_provider(self, name):
        """Return provider with specified name or raise an error.

        :param name: Provider's name.
        :type name: str

        :raise: :py:exc:`dependency_injector.errors.UndefinedProviderError`

        :return: Provider with specified name.
        :rtype: :py:class:`dependency_injector.providers.Provider`
        """
        try:
            return self.providers[name]
        except KeyError:
            raise Error('Provider "{0}" is not a part of {1}'.format(name,
                                                                     self))

    def has_provider(self, name):
        """Check if there is provider with certain name.

        :param name: Provider's name.
        :type name: str

        :rtype: bool
        """
        return name in self.providers

    def __getattr__(self, item):
        """Return provider with specified name or raise en error.

        :param name: Attribute's name.
        :type name: str

        :raise: :py:exc:`dependency_injector.errors.UndefinedProviderError`
        """
        if item.startswith('__') and item.endswith('__'):
            return super(CatalogBundle, self).__getattr__(item)
        raise UndefinedProviderError('Provider "{0}" is not a part '
                                     'of {1}'.format(item, self))

    def __repr__(self):
        """Return string representation of catalog's bundle.

        :rtype: str
        """
        return '<{0}.Bundle({1})>'.format(
            self.catalog.name, ', '.join(six.iterkeys(self.providers)))

    __str__ = __repr__


@six.python_2_unicode_compatible
class DynamicCatalog(object):
    """Dynamic catalog of providers.

    :py:class:`DynamicCatalog` is a catalog of providers that could be created
    in application's runtime. It should cover most of the cases when list of
    providers that would be included in catalog is non-deterministic in terms
    of apllication code (catalog's structure could be determined just after
    application will be started and will do some initial work, like parsing
    list of catalog's providers from the configuration).

    .. code-block:: python

        services = DynamicCatalog(auth=providers.Factory(AuthService),
                                  users=providers.Factory(UsersService))

        users_service = services.users()

    .. py:attribute:: Bundle

        Catalog's bundle class.

        :type: :py:class:`CatalogBundle`

    .. py:attribute:: name

        Catalog's name.

        By default, it is catalog's module + catalog's class name.

        :type: str

    .. py:attribute:: providers

        Dictionary of all providers.

        :type: dict[str, :py:class:`dependency_injector.providers.Provider`]

    .. py:attribute:: overridden_by

        Tuple of overriding catalogs.

        :type: tuple[
            :py:class:`DeclarativeCatalog` | :py:class:`DynamicCatalog`]

    .. py:attribute:: provider_type

        If provider type is defined, :py:class:`DynamicCatalog` checks that
        all of its providers are instances of
        :py:attr:`DynamicCatalog.provider_type`.

        :type: type | None
    """

    provider_type = None

    __IS_CATALOG__ = True
    __slots__ = ('name', 'providers', 'provider_names', 'overridden_by',
                 'Bundle')

    def __init__(self, **providers):
        """Initializer.

        :param providers: Dictionary of catalog providers.
        :type providers:
            dict[str, :py:class:`dependency_injector.providers.Provider`]
        """
        self.Bundle = CatalogBundle.sub_cls_factory(self)
        self.name = '.'.join((self.__class__.__module__,
                              self.__class__.__name__))
        self.providers = dict()
        self.provider_names = dict()
        self.overridden_by = tuple()
        self.bind_providers(providers)
        super(DynamicCatalog, self).__init__()

    def is_bundle_owner(self, bundle):
        """Check if catalog is bundle owner.

        :param bundle: Catalog's bundle instance.
        :type bundle: :py:class:`CatalogBundle`

        :rtype: bool
        """
        return ensure_is_catalog_bundle(bundle) and bundle.catalog is self

    def get_provider_bind_name(self, provider):
        """Return provider's name in catalog.

        :param provider: Provider instance.
        :type provider: :py:class:`dependency_injector.providers.Provider`

        :raise: :py:exc:`dependency_injector.errors.UndefinedProviderError`

        :return: Provider's name.
        :rtype: str
        """
        if not self.is_provider_bound(provider):
            raise Error('Can not find bind name for {0} in catalog {1}'.format(
                provider, self))
        return self.provider_names[provider]

    def is_provider_bound(self, provider):
        """Check if provider is bound to the catalog.

        :param provider: Provider instance.
        :type provider: :py:class:`dependency_injector.providers.Provider`

        :rtype: bool
        """
        return provider in self.provider_names

    def filter(self, provider_type):
        """Return dictionary of providers, that are instance of provided type.

        :param provider_type: Provider's type.
        :type provider_type: :py:class:`dependency_injector.providers.Provider`

        :rtype: dict[str, :py:class:`dependency_injector.providers.Provider`]
        """
        return dict((name, provider)
                    for name, provider in six.iteritems(self.providers)
                    if isinstance(provider, provider_type))

    @property
    def is_overridden(self):
        """Read-only property that is set to ``True`` if catalog is overridden.

        :rtype: bool
        """
        return bool(self.overridden_by)

    @property
    def last_overriding(self):
        """Read-only reference to the last overriding catalog, if any.

        :type: :py:class:`DeclarativeCatalog` | :py:class:`DynamicCatalog` |
               None
        """
        return self.overridden_by[-1] if self.overridden_by else None

    def override(self, overriding):
        """Override current catalog providers by overriding catalog providers.

        :param overriding: Overriding catalog.
        :type overriding: :py:class:`DeclarativeCatalog` |
                          :py:class:`DynamicCatalog`

        :raise: :py:exc:`dependency_injector.errors.Error` if trying to
                override catalog by itself

        :rtype: None
        """
        if overriding is self:
            raise Error('Catalog {0} could not be overridden '
                        'with itself'.format(self))
        self.overridden_by += (overriding,)
        for name, provider in six.iteritems(overriding.providers):
            self.get_provider(name).override(provider)

    def reset_last_overriding(self):
        """Reset last overriding catalog.

        :rtype: None
        """
        if not self.is_overridden:
            raise Error('Catalog {0} is not overridden'.format(self))
        self.overridden_by = self.overridden_by[:-1]
        for provider in six.itervalues(self.providers):
            provider.reset_last_overriding()

    def reset_override(self):
        """Reset all overridings for all catalog providers.

        :rtype: None
        """
        self.overridden_by = tuple()
        for provider in six.itervalues(self.providers):
            provider.reset_override()

    def get_provider(self, name):
        """Return provider with specified name or raise an error.

        :param name: Provider's name.
        :type name: str

        :raise: :py:exc:`dependency_injector.errors.UndefinedProviderError`

        :return: Provider with specified name.
        :rtype: :py:class:`dependency_injector.providers.Provider`
        """
        try:
            return self.providers[name]
        except KeyError:
            raise UndefinedProviderError('{0} has no provider with such '
                                         'name - {1}'.format(self, name))

    def bind_provider(self, name, provider):
        """Bind provider to catalog with specified name.

        :param name: Name of the provider.
        :type name: str

        :param provider: Provider instance.
        :type provider: :py:class:`dependency_injector.providers.Provider`

        :raise: :py:exc:`dependency_injector.errors.Error`

        :rtype: None
        """
        provider = ensure_is_provider(provider)

        if (self.__class__.provider_type and
                not isinstance(provider, self.__class__.provider_type)):
            raise Error('{0} can contain only {1} instances'.format(
                self, self.__class__.provider_type))

        if name in self.providers:
            raise Error('Catalog {0} already has provider with '
                        'such name - {1}'.format(self, name))
        if provider in self.provider_names:
            raise Error('Catalog {0} already has such provider '
                        'instance - {1}'.format(self, provider))

        self.providers[name] = provider
        self.provider_names[provider] = name

    def bind_providers(self, providers):
        """Bind providers dictionary to catalog.

        :param providers: Dictionary of providers, where key is a name
            and value is a provider.
        :type providers:
            dict[str, :py:class:`dependency_injector.providers.Provider`]

        :raise: :py:exc:`dependency_injector.errors.Error`

        :rtype: None
        """
        for name, provider in six.iteritems(providers):
            self.bind_provider(name, provider)

    def has_provider(self, name):
        """Check if there is provider with certain name.

        :param name: Provider's name.
        :type name: str

        :rtype: bool
        """
        return name in self.providers

    def unbind_provider(self, name):
        """Remove provider binding.

        :param name: Provider's name.
        :type name: str

        :rtype: None
        """
        provider = self.get_provider(name)
        del self.providers[name]
        del self.provider_names[provider]

    def __getattr__(self, name):
        """Return provider with specified name or raise en error.

        :param name: Attribute's name.
        :type name: str

        :raise: :py:exc:`dependency_injector.errors.UndefinedProviderError`
        """
        return self.get_provider(name)

    def __setattr__(self, name, value):
        """Handle setting of catalog attributes.

        Setting of attributes works as usual, but if value of attribute is
        provider, this provider will be bound to catalog.

        :param name: Attribute's name.
        :type name: str

        :param value: Attribute's value.
        :type value: :py:class:`dependency_injector.providers.Provider` |
                     object

        :rtype: None
        """
        if is_provider(value):
            return self.bind_provider(name, value)
        return super(DynamicCatalog, self).__setattr__(name, value)

    def __delattr__(self, name):
        """Handle deleting of catalog attibute.

        Deleting of attributes works as usual, but if value of attribute is
        provider, this provider will be unbound from catalog.

        :param name: Attribute's name.
        :type name: str

        :rtype: None
        """
        self.unbind_provider(name)

    def __repr__(self):
        """Return Python representation of catalog.

        :rtype: str
        """
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

        if cls.provider_type:
            cls._catalog = type('DynamicCatalog',
                                (DynamicCatalog,),
                                dict(provider_type=cls.provider_type))()
        else:
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
            :py:class:`DeclarativeCatalog` |
            :py:class:`DynamicCatalog`]
        """
        return cls._catalog.overridden_by

    @property
    def is_overridden(cls):
        """Read-only property that is set to ``True`` if catalog is overridden.

        :rtype: bool
        """
        return cls._catalog.is_overridden

    @property
    def last_overriding(cls):
        """Read-only reference to the last overriding catalog, if any.

        :type: :py:class:`DeclarativeCatalog` | :py:class:`DynamicCatalog` |
               None
        """
        return cls._catalog.last_overriding

    def __getattr__(cls, name):
        """Return provider with specified name or raise en error.

        :param name: Attribute's name.
        :type name: str

        :raise: :py:exc:`dependency_injector.errors.UndefinedProviderError`
        """
        raise UndefinedProviderError('There is no provider "{0}" in '
                                     'catalog {1}'.format(name, cls))

    def __setattr__(cls, name, value):
        """Handle setting of catalog attributes.

        Setting of attributes works as usual, but if value of attribute is
        provider, this provider will be bound to catalog.

        :param name: Attribute's name.
        :type name: str

        :param value: Attribute's value.
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

        :param name: Attribute's name.
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

    :py:class:`DeclarativeCatalog` is a catalog of providers that could be
    defined in declarative manner. It should cover most of the cases when list
    of providers that would be included in catalog is deterministic (catalog
    will not change its structure in runtime).

    .. code-block:: python

        class Services(DeclarativeCatalog):

            auth = providers.Factory(AuthService)

            users = providers.Factory(UsersService)

        users_service = Services.users()

    .. py:attribute:: Bundle

        Catalog's bundle class.

        :type: :py:class:`CatalogBundle`

    .. py:attribute:: name

        Read-only property that represents catalog's name.

        Catalog's name is catalog's module + catalog's class name.

        :type: str

    .. py:attribute:: cls_providers

        Read-only dictionary of current catalog providers.

        :type: dict[str, :py:class:`dependency_injector.providers.Provider`]

    .. py:attribute:: inherited_providers

        Read-only dictionary of inherited providers.

        :type: dict[str, :py:class:`dependency_injector.providers.Provider`]

    .. py:attribute:: providers

        Read-only dictionary of all providers.

        :type: dict[str, :py:class:`dependency_injector.providers.Provider`]

    .. py:attribute:: overridden_by

        Tuple of overriding catalogs.

        :type: tuple[:py:class:`DeclarativeCatalog` |
                    :py:class:`DynamicCatalog`]

    .. py:attribute:: is_overridden

        Read-only property that is set to ``True`` if catalog is overridden.

        :type: bool

    .. py:attribute:: is_overridden

        Read-only reference to the last overriding catalog, if any.

        :type: :py:class:`DeclarativeCatalog` | :py:class:`DynamicCatalog` |
               None

    .. py:attribute:: provider_type

        If provider type is defined, :py:class:`DeclarativeCatalog` checks that
        all of its providers are instances of
        :py:attr:`DeclarativeCatalog.provider_type`.

        :type: type | None
    """

    Bundle = CatalogBundle

    name = str()

    cls_providers = dict()
    inherited_providers = dict()
    providers = dict()

    overridden_by = tuple()
    is_overridden = bool
    last_overriding = None

    provider_type = None

    _catalog = DynamicCatalog

    __IS_CATALOG__ = True

    @classmethod
    def is_bundle_owner(cls, bundle):
        """Check if catalog is bundle owner.

        :param bundle: Catalog's bundle instance.
        :type bundle: :py:class:`CatalogBundle`

        :rtype: bool
        """
        return cls._catalog.is_bundle_owner(bundle)

    @classmethod
    def get_provider_bind_name(cls, provider):
        """Return provider's name in catalog.

        :param provider: Provider instance.
        :type provider: :py:class:`dependency_injector.providers.Provider`

        :raise: :py:exc:`dependency_injector.errors.UndefinedProviderError`

        :return: Provider's name.
        :rtype: str
        """
        return cls._catalog.get_provider_bind_name(provider)

    @classmethod
    def is_provider_bound(cls, provider):
        """Check if provider is bound to the catalog.

        :param provider: Provider instance.
        :type provider: :py:class:`dependency_injector.providers.Provider`

        :rtype: bool
        """
        return cls._catalog.is_provider_bound(provider)

    @classmethod
    def filter(cls, provider_type):
        """Return dictionary of providers, that are instance of provided type.

        :param provider_type: Provider's type.
        :type provider_type: :py:class:`dependency_injector.providers.Provider`

        :rtype: dict[str, :py:class:`dependency_injector.providers.Provider`]
        """
        return cls._catalog.filter(provider_type)

    @classmethod
    def override(cls, overriding):
        """Override current catalog providers by overriding catalog providers.

        :param overriding: Overriding catalog.
        :type overriding: :py:class:`DeclarativeCatalog` |
                          :py:class:`DynamicCatalog`

        :raise: :py:exc:`dependency_injector.errors.Error` if trying to
                override catalog by itself or its subclasses

        :rtype: None
        """
        if is_declarative_catalog(overriding) and issubclass(cls, overriding):
            raise Error('Catalog {0} could not be overridden '
                        'with itself or its subclasses'.format(cls))
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

        :param name: Provider's name.
        :type name: str

        :raise: :py:exc:`dependency_injector.errors.UndefinedProviderError`

        :return: Provider with specified name.
        :rtype: :py:class:`dependency_injector.providers.Provider`
        """
        return cls._catalog.get_provider(name)

    get = get_provider  # Backward compatibility for versions < 0.11.*

    @classmethod
    def bind_provider(cls, name, provider):
        """Bind provider to catalog with specified name.

        :param name: Name of the provider.
        :type name: str

        :param provider: Provider instance.
        :type provider: :py:class:`dependency_injector.providers.Provider`

        :raise: :py:exc:`dependency_injector.errors.Error`

        :rtype: None
        """
        setattr(cls, name, provider)

    @classmethod
    def bind_providers(cls, providers):
        """Bind providers dictionary to catalog.

        :param providers: Dictionary of providers, where key is a name
            and value is a provider.
        :type providers:
            dict[str, :py:class:`dependency_injector.providers.Provider`]

        :raise: :py:exc:`dependency_injector.errors.Error`

        :rtype: None
        """
        for name, provider in six.iteritems(providers):
            setattr(cls, name, provider)

    @classmethod
    def has_provider(cls, name):
        """Check if there is provider with certain name.

        :param name: Provider's name.
        :type name: str

        :rtype: bool
        """
        return hasattr(cls, name)

    has = has_provider  # Backward compatibility for versions < 0.11.*

    @classmethod
    def unbind_provider(cls, name):
        """Remove provider binding.

        :param name: Provider's name.
        :type name: str

        :rtype: None
        """
        delattr(cls, name)

    @classmethod
    def __getattr__(cls, name):  # pragma: no cover
        """Return provider with specified name or raise en error.

        :param name: Attribute's name.
        :type name: str

        :raise: :py:exc:`dependency_injector.errors.UndefinedProviderError`
        """
        raise NotImplementedError('Implementated in metaclass')

    @classmethod
    def __setattr__(cls, name, value):  # pragma: no cover
        """Handle setting of catalog attributes.

        Setting of attributes works as usual, but if value of attribute is
        provider, this provider will be bound to catalog.

        :param name: Attribute's name.
        :type name: str

        :param value: Attribute's value.
        :type value: :py:class:`dependency_injector.providers.Provider` |
                     object

        :rtype: None
        """
        raise NotImplementedError('Implementated in metaclass')

    @classmethod
    def __delattr__(cls, name):  # pragma: no cover
        """Handle deleting of catalog attibute.

        Deleting of attributes works as usual, but if value of attribute is
        provider, this provider will be unbound from catalog.

        :param name: Attribute's name.
        :type name: str

        :rtype: None
        """
        raise NotImplementedError('Implementated in metaclass')


# Backward compatibility for versions < 0.11.*
AbstractCatalog = DeclarativeCatalog


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
