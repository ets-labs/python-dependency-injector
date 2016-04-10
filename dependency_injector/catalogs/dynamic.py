"""Dependency injector dynamic catalog module."""

import copy

import six

from dependency_injector.catalogs.bundle import CatalogBundle
from dependency_injector.utils import (
    is_provider,
    ensure_is_provider,
    ensure_is_catalog_bundle,
)
from dependency_injector.errors import (
    Error,
    UndefinedProviderError,
)


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

    def bind_provider(self, name, provider, force=False):
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
        provider = ensure_is_provider(provider)

        if (self.__class__.provider_type and
                not isinstance(provider, self.__class__.provider_type)):
            raise Error('{0} can contain only {1} instances'.format(
                self, self.__class__.provider_type))

        if not force:
            if name in self.providers:
                raise Error('Catalog {0} already has provider with '
                            'such name - {1}'.format(self, name))
            if provider in self.provider_names:
                raise Error('Catalog {0} already has such provider '
                            'instance - {1}'.format(self, provider))

        self.providers[name] = provider
        self.provider_names[provider] = name

    def bind_providers(self, providers, force=False):
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
            self.bind_provider(name, provider, force)

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

    def copy(self):
        """Copy catalog instance and return it.

        :rtype: py:class:`DynamicCatalog`
        :return: Copied catalog.
        """
        return copy.copy(self)

    def deepcopy(self, memo=None):
        """Copy catalog instance and it's providers and return it.

        :param memo: Memorized instances
        :type memo: dict[int, object]

        :rtype: py:class:`DynamicCatalog`
        :return: Copied catalog.
        """
        return copy.deepcopy(self, memo)

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
