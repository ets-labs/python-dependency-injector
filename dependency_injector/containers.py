"""IoC containers module."""

import six

from dependency_injector import (
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
                                    for base in bases if utils.is_catalog(base)
                                    for name, provider in six.iteritems(
                                        base.cls_providers))

        attributes['cls_providers'] = dict(cls_providers)
        attributes['inherited_providers'] = dict(inherited_providers)
        attributes['providers'] = dict(cls_providers + inherited_providers)

        return type.__new__(mcs, class_name, bases, attributes)

    def __setattr__(cls, name, value):
        """Set class attribute.

        If value of attribute is provider, it will be added into providers
        dictionary.
        """
        if utils.is_provider(value):
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


@six.add_metaclass(DeclarativeContainerMetaClass)
class DeclarativeContainer(object):
    """Declarative inversion of control container."""

    __IS_CATALOG__ = True

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
            raise errors.Error('Catalog {0} could not be overridden '
                               'with itself or its subclasses'.format(cls))

        cls.overridden_by += (overriding,)

        for name, provider in six.iteritems(overriding.cls_providers):
            try:
                getattr(cls, name).override(provider)
            except AttributeError:
                pass


def override(container):
    """:py:class:`DeclarativeContainer` overriding decorator.

    :param catalog: Container that should be overridden by decorated container.
    :type catalog: :py:class:`DeclarativeContainer`

    :return: Declarative container's overriding decorator.
    :rtype: callable(:py:class:`DeclarativeContainer`)
    """
    def decorator(overriding_container):
        """Overriding decorator."""
        container.override(overriding_container)
        return overriding_container
    return decorator
