"""Catalog module."""

from six import iteritems

from .errors import Error
from .utils import is_provider


class CatalogMetaClass(type):

    """Providers catalog meta class."""

    def __new__(mcs, class_name, bases, attributes):
        """Meta class factory."""
        providers = dict()
        new_attributes = dict()
        for name, value in attributes.iteritems():
            if is_provider(value):
                providers[name] = value
            new_attributes[name] = value

        cls = type.__new__(mcs, class_name, bases, new_attributes)
        cls.providers = cls.providers.copy()
        cls.providers.update(providers)
        return cls


class AbstractCatalog(object):

    """Abstract providers catalog."""

    providers = dict()

    __slots__ = ('providers', '__used_providers__',)
    __metaclass__ = CatalogMetaClass

    def __init__(self, *used_providers):
        """Initializer."""
        self.__used_providers__ = set(used_providers)

    def __getattribute__(self, item):
        """Return providers."""
        attribute = super(AbstractCatalog, self).__getattribute__(item)
        if item in ('providers', '__used_providers__',):
            return attribute

        if attribute not in self.__used_providers__:
            raise Error('Provider \'{0}\' '.format(item) +
                        'is not listed in dependencies')
        return attribute

    @classmethod
    def filter(cls, provider_type):
        """Return dict of providers, that are instance of provided type."""
        return dict([(name, provider)
                     for name, provider in iteritems(cls.providers)
                     if isinstance(provider, provider_type)])

    @classmethod
    def override(cls, overriding):
        """Override current catalog providers by overriding catalog providers.

        :type overriding: AbstractCatalog
        """
        for name, provider in iteritems(overriding.providers):
            cls.providers[name].override(provider)
