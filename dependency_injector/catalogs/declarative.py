"""Dependency injector declarative catalog module."""

import six

from dependency_injector.catalogs.dynamic import DynamicCatalog
from dependency_injector.catalogs.bundle import CatalogBundle
from dependency_injector.utils import (
    is_provider,
    is_catalog,
    is_declarative_catalog,
)
from dependency_injector.errors import (
    Error,
    UndefinedProviderError,
)


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

        cls._cls_providers = dict(cls_providers)
        cls._inherited_providers = dict(inherited_providers)

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
    def cls_providers(cls):
        """Read-only dictionary of current catalog providers.

        :rtype: dict[str, :py:class:`dependency_injector.providers.Provider`]
        """
        return cls._cls_providers

    @property
    def inherited_providers(cls):
        """Read-only dictionary of inherited providers.

        :rtype: dict[str, :py:class:`dependency_injector.providers.Provider`]
        """
        return cls._inherited_providers

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
            cls.bind_provider(name, value, _set_as_attribute=False)
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

    .. py:attribute:: provider_type

        If provider type is defined, :py:class:`DeclarativeCatalog` checks that
        all of its providers are instances of
        :py:attr:`DeclarativeCatalog.provider_type`.

        :type: type | None
    """

    Bundle = CatalogBundle

    provider_type = None

    _catalog = DynamicCatalog

    _cls_providers = dict()
    _inherited_providers = dict()

    __IS_CATALOG__ = True

    @property
    def name(self):
        """Read-only property that represents catalog's name.

        Catalog's name is catalog's module + catalog's class name.

        :rtype: str
        """
        return self.__class__.name

    @property
    def providers(self):
        """Read-only dictionary of all providers.

        :rtype: dict[str, :py:class:`dependency_injector.providers.Provider`]
        """
        return self.__class__.providers

    @property
    def cls_providers(self):
        """Read-only dictionary of current catalog providers.

        :rtype: dict[str, :py:class:`dependency_injector.providers.Provider`]
        """
        return self.__class__.cls_providers

    @property
    def inherited_providers(self):
        """Read-only dictionary of inherited providers.

        :rtype: dict[str, :py:class:`dependency_injector.providers.Provider`]
        """
        return self.__class__.inherited_providers

    @property
    def overridden_by(self):
        """Tuple of overriding catalogs.

        :rtype: tuple[:py:class:`DeclarativeCatalog` |
                      :py:class:`DynamicCatalog`]
        """
        return self.__class__.overridden_by

    @property
    def is_overridden(self):
        """Read-only property that is set to ``True`` if catalog is overridden.

        :rtype: bool
        """
        return self.__class__.is_overridden

    @property
    def last_overriding(self):
        """Read-only reference to the last overriding catalog, if any.

        :rtype: :py:class:`DeclarativeCatalog` | :py:class:`DynamicCatalog` |
               None
        """
        return self.__class__.last_overriding

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

    @classmethod
    def bind_provider(cls, name, provider, force=False,
                      _set_as_attribute=True):
        """Bind provider to catalog with specified name.

        :param name: Name of the provider.
        :type name: str

        :param provider: Provider instance.
        :type provider: :py:class:`dependency_injector.providers.Provider`

        :param force: Force binding of provider.
        :type force: bool

        :raise: :py:exc:`dependency_injector.errors.Error`

        :rtype: None
        """
        if cls._catalog.is_provider_bound(provider):
            bindind_name = cls._catalog.get_provider_bind_name(provider)
            if bindind_name == name and not force:
                return

        cls._catalog.bind_provider(name, provider, force)
        cls.cls_providers[name] = provider

        if _set_as_attribute:
            setattr(cls, name, provider)

    @classmethod
    def bind_providers(cls, providers, force=False):
        """Bind providers dictionary to catalog.

        :param providers: Dictionary of providers, where key is a name
            and value is a provider.
        :type providers:
            dict[str, :py:class:`dependency_injector.providers.Provider`]

        :param force: Force binding of providers.
        :type force: bool

        :raise: :py:exc:`dependency_injector.errors.Error`

        :rtype: None
        """
        for name, provider in six.iteritems(providers):
            cls.bind_provider(name, provider, force=force)

    @classmethod
    def has_provider(cls, name):
        """Check if there is provider with certain name.

        :param name: Provider's name.
        :type name: str

        :rtype: bool
        """
        return hasattr(cls, name)

    @classmethod
    def unbind_provider(cls, name):
        """Remove provider binding.

        :param name: Provider's name.
        :type name: str

        :rtype: None
        """
        delattr(cls, name)
        del cls.cls_providers[name]

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
