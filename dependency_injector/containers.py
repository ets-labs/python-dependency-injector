"""IoC containers module."""

import six

from dependency_injector import (
    providers,
    utils,
    errors,
)


class DeclarativeContainerMetaClass(type):
    """Declarative inversion of control container meta class."""

    def __new__(mcs, class_name, bases, attributes):
        """Declarative container class factory."""
        cls_providers = tuple((name, provider)
                              for name, provider in six.iteritems(attributes)
                              if utils.is_provider(provider))

        inherited_providers = tuple((name, provider)
                                    for base in bases if utils.is_container(
                                        base)
                                    for name, provider in six.iteritems(
                                        base.cls_providers))

        attributes['cls_providers'] = dict(cls_providers)
        attributes['inherited_providers'] = dict(inherited_providers)
        attributes['providers'] = dict(cls_providers + inherited_providers)

        cls = type.__new__(mcs, class_name, bases, attributes)

        for provider in six.itervalues(cls.providers):
            cls._check_provider_type(provider)

        return cls

    def __setattr__(cls, name, value):
        """Set class attribute.

        If value of attribute is provider, it will be added into providers
        dictionary.
        """
        if utils.is_provider(value):
            cls._check_provider_type(value)
            cls.providers[name] = value
            cls.cls_providers[name] = value
        super(DeclarativeContainerMetaClass, cls).__setattr__(name, value)

    def __delattr__(cls, name):
        """Delete class attribute.

        If value of attribute is provider, it will be deleted from providers
        dictionary.
        """
        if name in cls.providers and name in cls.cls_providers:
            del cls.providers[name]
            del cls.cls_providers[name]
        super(DeclarativeContainerMetaClass, cls).__delattr__(name)

    def _check_provider_type(cls, provider):
        if not isinstance(provider, cls.provider_type):
            raise errors.Error('{0} can contain only {1} '
                               'instances'.format(cls, cls.provider_type))


@six.add_metaclass(DeclarativeContainerMetaClass)
class DeclarativeContainer(object):
    """Declarative inversion of control container."""

    __IS_CONTAINER__ = True

    provider_type = providers.Provider

    providers = dict()
    cls_providers = dict()
    inherited_providers = dict()

    overridden_by = tuple()

    @classmethod
    def override(cls, overriding):
        """Override current container by overriding container.

        :param overriding: Overriding container.
        :type overriding: :py:class:`DeclarativeContainer`

        :raise: :py:exc:`dependency_injector.errors.Error` if trying to
                override container by itself or its subclasses

        :rtype: None
        """
        if issubclass(cls, overriding):
            raise errors.Error('Container {0} could not be overridden '
                               'with itself or its subclasses'.format(cls))

        cls.overridden_by += (overriding,)

        for name, provider in six.iteritems(overriding.cls_providers):
            try:
                getattr(cls, name).override(provider)
            except AttributeError:
                pass

    @classmethod
    def reset_last_overriding(cls):
        """Reset last overriding provider for each container providers.

        :rtype: None
        """
        if not cls.overridden_by:
            raise errors.Error('Container {0} is not overridden'.format(cls))

        cls.overridden_by = cls.overridden_by[:-1]

        for provider in six.itervalues(cls.providers):
            provider.reset_last_overriding()

    @classmethod
    def reset_override(cls):
        """Reset all overridings for each container providers.

        :rtype: None
        """
        cls.overridden_by = tuple()

        for provider in six.itervalues(cls.providers):
            provider.reset_override()


def override(container):
    """:py:class:`DeclarativeContainer` overriding decorator.

    :param container: Container that should be overridden by decorated
                      container.
    :type container: :py:class:`DeclarativeContainer`

    :return: Declarative container's overriding decorator.
    :rtype: callable(:py:class:`DeclarativeContainer`)
    """
    def _decorator(overriding_container):
        """Overriding decorator."""
        container.override(overriding_container)
        return overriding_container
    return _decorator


def copy(container):
    """:py:class:`DeclarativeContainer` copying decorator.

    This decorator copy all providers from provided container to decorated one.
    If one of the decorated container providers matches to source container
    providers by name, it would be replaced by reference.

    :param container: Container that should be copied by decorated container.
    :type container :py:class:`DeclarativeContainer`

    :return: Declarative container's copying decorator.
    :rtype: callable(:py:class:`DeclarativeContainer`)
    """
    def _decorator(copied_container):
        memo = dict()
        for name, provider in six.iteritems(copied_container.cls_providers):
            try:
                source_provider = getattr(container, name)
            except AttributeError:
                pass
            else:
                memo[id(source_provider)] = provider

        providers_copy = utils._copy_providers(container.providers, memo)
        for name, provider in six.iteritems(providers_copy):
            setattr(copied_container, name, provider)

        return copied_container
    return _decorator
