"""IoC containers module."""

import six

from dependency_injector import utils


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

        return type.__new__(mcs, class_name, bases, attributes)

    def __setattr__(cls, name, value):
        """Set class attribute.

        If value of attribute is provider, it will be added into providers
        dictionary.
        """
        if utils.is_provider(value):
            cls.providers[name] = value
        super(DeclarativeContainerMetaClass, cls).__setattr__(name, value)


class Container(object):
    """Inversion of control container."""

    __IS_CATALOG__ = True

    def __init__(self):
        """Initializer."""
        self.providers = dict()

    def bind_providers(self, **providers):
        """Bind providers to the container."""
        for name, provider in six.iteritems(providers):
            setattr(self, name, utils.ensure_is_provider(provider))
        return self

    def __setattr__(self, name, value):
        """Set instance attribute.

        If value of attribute is provider, it will be added into providers
        dictionary.
        """
        if utils.is_provider(value):
            self.providers[name] = value
        super(Container, self).__setattr__(name, value)


@six.add_metaclass(DeclarativeContainerMetaClass)
class DeclarativeContainer(object):
    """Declarative inversion of control container."""

    cls_providers = dict()
    inherited_providers = dict()

    def __init__(self):
        """Initializer."""
        self.providers = dict()
        self.providers.update(self.__class__.inherited_providers)
        self.providers.update(self.__class__.cls_providers)
        super(DeclarativeContainer, self).__init__()


def override(declarative_container):
    """:py:class:`DeclarativeContainer` overriding decorator.

    :param declarative_container: Container that should be overridden by
                                  decorated container.
    :type declarative_container: :py:class:`DeclarativeContainer`

    :return: Declarative container's overriding decorator.
    :rtype: callable(:py:class:`DeclarativeContainer`)
    """
    def decorator(overriding_container):
        """Overriding decorator."""
        declarative_container.override(overriding_container)
        return overriding_container
    return decorator
