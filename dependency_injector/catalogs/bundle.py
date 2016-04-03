"""Dependency injector catalogs bundle module."""

import six

from dependency_injector.errors import (
    Error,
    UndefinedProviderError,
)


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
