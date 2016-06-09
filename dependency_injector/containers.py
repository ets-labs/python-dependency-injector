"""Dependency injector IoC containers module."""

import six

from dependency_injector import (
    providers,
    utils,
    errors,
)


class DynamicContainer(object):
    """Dynamic inversion of control container.

    .. code-block:: python

        services = DynamicContainer()
        services.auth = providers.Factory(AuthService)
        services.users = providers.Factory(UsersService,
                                           auth_service=services.auth)

    .. py:attribute:: providers

        Read-only dictionary of all providers.

        :type: dict[str, :py:class:`dependency_injector.providers.Provider`]

    .. py:attribute:: overridden

        Tuple of overriding containers.

        :type: tuple[:py:class:`DynamicContainer`]

    .. py:attribute:: provider_type

        Type of providers that could be placed in container.

        :type: type
    """

    __IS_CONTAINER__ = True

    def __init__(self):
        """Initializer.

        :rtype: None
        """
        self.provider_type = providers.Provider
        self.providers = dict()
        self.overridden = tuple()
        super(DynamicContainer, self).__init__()

    def __setattr__(self, name, value):
        """Set instance attribute.

        If value of attribute is provider, it will be added into providers
        dictionary.

        :param name: Attribute's name
        :type name: str

        :param value: Attribute's value
        :type value: object

        :rtype: None
        """
        if utils.is_provider(value):
            _check_provider_type(self, value)
            self.providers[name] = value
        super(DynamicContainer, self).__setattr__(name, value)

    def __delattr__(self, name):
        """Delete instance attribute.

        If value of attribute is provider, it will be deleted from providers
        dictionary.

        :param name: Attribute's name
        :type name: str

        :rtype: None
        """
        if name in self.providers:
            del self.providers[name]
        super(DynamicContainer, self).__delattr__(name)

    def override(self, overriding):
        """Override current container by overriding container.

        :param overriding: Overriding container.
        :type overriding: :py:class:`DynamicContainer`

        :raise: :py:exc:`dependency_injector.errors.Error` if trying to
                override container by itself

        :rtype: None
        """
        if overriding is self:
            raise errors.Error('Container {0} could not be overridden '
                               'with itself'.format(self))

        self.overridden += (overriding,)

        for name, provider in six.iteritems(overriding.providers):
            try:
                getattr(self, name).override(provider)
            except AttributeError:
                pass

    def reset_last_overriding(self):
        """Reset last overriding provider for each container providers.

        :rtype: None
        """
        if not self.overridden:
            raise errors.Error('Container {0} is not overridden'.format(self))

        self.overridden = self.overridden[:-1]

        for provider in six.itervalues(self.providers):
            provider.reset_last_overriding()

    def reset_override(self):
        """Reset all overridings for each container providers.

        :rtype: None
        """
        self.overridden = tuple()

        for provider in six.itervalues(self.providers):
            provider.reset_override()


class DeclarativeContainerMetaClass(type):
    """Declarative inversion of control container meta class."""

    def __new__(mcs, class_name, bases, attributes):
        """Declarative container class factory."""
        cls_providers = tuple((name, provider)
                              for name, provider in six.iteritems(attributes)
                              if utils.is_provider(provider))

        inherited_providers = tuple((name, provider)
                                    for base in bases if utils.is_container(
                                        base) and base is not DynamicContainer
                                    for name, provider in six.iteritems(
                                        base.cls_providers))

        attributes['cls_providers'] = dict(cls_providers)
        attributes['inherited_providers'] = dict(inherited_providers)
        attributes['providers'] = dict(cls_providers + inherited_providers)

        cls = type.__new__(mcs, class_name, bases, attributes)

        for provider in six.itervalues(cls.providers):
            _check_provider_type(cls, provider)

        return cls

    def __setattr__(cls, name, value):
        """Set class attribute.

        If value of attribute is provider, it will be added into providers
        dictionary.

        :param name: Attribute's name
        :type name: str

        :param value: Attribute's value
        :type value: object

        :rtype: None
        """
        if utils.is_provider(value):
            _check_provider_type(cls, value)
            cls.providers[name] = value
            cls.cls_providers[name] = value
        super(DeclarativeContainerMetaClass, cls).__setattr__(name, value)

    def __delattr__(cls, name):
        """Delete class attribute.

        If value of attribute is provider, it will be deleted from providers
        dictionary.

        :param name: Attribute's name
        :type name: str

        :rtype: None
        """
        if name in cls.providers and name in cls.cls_providers:
            del cls.providers[name]
            del cls.cls_providers[name]
        super(DeclarativeContainerMetaClass, cls).__delattr__(name)


@six.add_metaclass(DeclarativeContainerMetaClass)
class DeclarativeContainer(object):
    """Declarative inversion of control container.

    .. code-block:: python

        class Services(DeclarativeContainer):
            auth = providers.Factory(AuthService)
            users = providers.Factory(UsersService,
                                      auth_service=auth)
    """

    __IS_CONTAINER__ = True

    provider_type = providers.Provider
    """Type of providers that could be placed in container.

    :type: type
    """

    instance_type = DynamicContainer
    """Type of container that is returned on instantiating declarative
    container.

    :type: type
    """

    providers = dict()
    """Read-only dictionary of all providers.

    :type: dict[str, :py:class:`dependency_injector.providers.Provider`]
    """

    cls_providers = dict()
    """Read-only dictionary of current container providers.

    :type: dict[str, :py:class:`dependency_injector.providers.Provider`]
    """

    inherited_providers = dict()
    """Read-only dictionary of inherited providers.

    :type: dict[str, :py:class:`dependency_injector.providers.Provider`]
    """

    overridden = tuple()
    """Tuple of overriding containers.

    :type: tuple[:py:class:`DeclarativeContainer`]
    """

    def __new__(cls, *args, **kwargs):
        """Constructor.

        :return: Dynamic container with copy of all providers.
        :rtype: :py:class:`DynamicContainer`
        """
        container = cls.instance_type(*args, **kwargs)
        container.provider_type = cls.provider_type

        for name, provider in six.iteritems(utils.deepcopy(cls.providers)):
            setattr(container, name, provider)

        return container

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

        cls.overridden += (overriding,)

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
        if not cls.overridden:
            raise errors.Error('Container {0} is not overridden'.format(cls))

        cls.overridden = cls.overridden[:-1]

        for provider in six.itervalues(cls.providers):
            provider.reset_last_overriding()

    @classmethod
    def reset_override(cls):
        """Reset all overridings for each container providers.

        :rtype: None
        """
        cls.overridden = tuple()

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
    :type container: :py:class:`DeclarativeContainer`

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

        providers_copy = utils.deepcopy(container.providers, memo)
        for name, provider in six.iteritems(providers_copy):
            setattr(copied_container, name, provider)

        return copied_container
    return _decorator


def _check_provider_type(cls, provider):
    if not isinstance(provider, cls.provider_type):
        raise errors.Error('{0} can contain only {1} '
                           'instances'.format(cls, cls.provider_type))
