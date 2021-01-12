"""Containers module."""

import inspect
import sys

try:
    import asyncio
except ImportError:
    asyncio = None

import six

from .errors import Error
from .providers cimport (
    Provider,
    Object,
    Resource,
    deepcopy,
)


if sys.version_info[:2] >= (3, 6):
    from .wiring import wire, unwire
else:
    def wire(*args, **kwargs):
        raise NotImplementedError('Wiring requires Python 3.6 or above')

    def unwire(*args, **kwargs):
        raise NotImplementedError('Wiring requires Python 3.6 or above')


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
        self.provider_type = Provider
        self.providers = {}
        self.overridden = tuple()
        self.declarative_parent = None
        self.wired_to_modules = []
        self.wired_to_packages = []
        self.__self__ = Object(self)
        super(DynamicContainer, self).__init__()

    def __deepcopy__(self, memo):
        """Create and return full copy of container."""
        copied = memo.get(id(self))
        if copied is not None:
            return copied

        copied = self.__class__()
        copied.provider_type = Provider
        copied.overridden = deepcopy(self.overridden, memo)
        copied.declarative_parent = self.declarative_parent

        for name, provider in deepcopy(self.providers, memo).items():
            setattr(copied, name, provider)

        return copied

    def __setattr__(self, str name, object value):
        """Set instance attribute.

        If value of attribute is provider, it will be added into providers
        dictionary.

        :param name: Attribute's name
        :type name: str

        :param value: Attribute's value
        :type value: object

        :rtype: None
        """
        if isinstance(value, Provider) and name != '__self__':
            _check_provider_type(self, value)
            self.providers[name] = value
        super(DynamicContainer, self).__setattr__(name, value)

    def __delattr__(self, str name):
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

    def set_providers(self, **providers):
        """Set container providers.

        :param providers: Dictionary of providers
        :type providers:
            dict[str, :py:class:`dependency_injector.providers.Provider`]

        :rtype: None
        """
        for name, provider in six.iteritems(providers):
            setattr(self, name, provider)

    def override(self, object overriding):
        """Override current container by overriding container.

        :param overriding: Overriding container.
        :type overriding: :py:class:`DynamicContainer`

        :raise: :py:exc:`dependency_injector.errors.Error` if trying to
                override container by itself

        :rtype: None
        """
        if overriding is self:
            raise Error('Container {0} could not be overridden '
                        'with itself'.format(self))

        self.overridden += (overriding,)

        for name, provider in six.iteritems(overriding.providers):
            try:
                getattr(self, name).override(provider)
            except AttributeError:
                pass

    def override_providers(self, **overriding_providers):
        """Override container providers.

        :param overriding_providers: Dictionary of providers
        :type overriding_providers:
            dict[str, :py:class:`dependency_injector.providers.Provider`]

        :rtype: None
        """
        for name, overriding_provider in six.iteritems(overriding_providers):
            container_provider = getattr(self, name)
            container_provider.override(overriding_provider)

    def reset_last_overriding(self):
        """Reset last overriding provider for each container providers.

        :rtype: None
        """
        if not self.overridden:
            raise Error('Container {0} is not overridden'.format(self))

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

    def wire(self, modules=None, packages=None):
        """Wire container providers with provided packages and modules.

        :rtype: None
        """
        wire(
            container=self,
            modules=modules,
            packages=packages,
        )

        if modules:
            self.wired_to_modules.extend(modules)

        if packages:
            self.wired_to_packages.extend(packages)

    def unwire(self):
        """Unwire container providers from previously wired packages and modules."""
        unwire(
            modules=self.wired_to_modules,
            packages=self.wired_to_packages,
        )

        self.wired_to_modules.clear()
        self.wired_to_packages.clear()

    def init_resources(self):
        """Initialize all container resources."""
        futures = []
        for provider in self.providers.values():
            if not isinstance(provider, Resource):
                continue

            resource = provider.init()

            if _isawaitable(resource):
                futures.append(resource)

        if futures:
            return asyncio.gather(*futures)

    def shutdown_resources(self):
        """Shutdown all container resources."""
        futures = []
        for provider in self.providers.values():
            if not isinstance(provider, Resource):
                continue

            shutdown = provider.shutdown()

            if _isawaitable(shutdown):
                futures.append(shutdown)

        if futures:
            return asyncio.gather(*futures)


class DeclarativeContainerMetaClass(type):
    """Declarative inversion of control container meta class."""

    def __new__(type mcs, str class_name, tuple bases, dict attributes):
        """Declarative container class factory."""
        cdef tuple cls_providers
        cdef tuple inherited_providers
        cdef type cls

        containers = tuple(
            (name, container)
            for name, container in six.iteritems(attributes)
            if is_container(container)
        )

        attributes['containers'] = dict(containers)

        cls_providers = tuple(
            (name, provider)
            for name, provider in six.iteritems(attributes)
            if isinstance(provider, Provider)
        )

        inherited_providers = tuple(
            (name, provider)
            for base in bases
            if is_container(base) and base is not DynamicContainer
            for name, provider in six.iteritems(base.providers)
        )

        attributes['cls_providers'] = dict(cls_providers)
        attributes['inherited_providers'] = dict(inherited_providers)
        attributes['providers'] = dict(cls_providers + inherited_providers)

        cls = <type>type.__new__(mcs, class_name, bases, attributes)

        cls.__self__ = Object(cls)

        for provider in six.itervalues(cls.providers):
            _check_provider_type(cls, provider)

        return cls

    def __setattr__(cls, str name, object value):
        """Set class attribute.

        If value of attribute is provider, it will be added into providers
        dictionary.

        :param name: Attribute's name
        :type name: str

        :param value: Attribute's value
        :type value: object

        :rtype: None
        """
        if isinstance(value, Provider) and name != '__self__':
            _check_provider_type(cls, value)
            cls.providers[name] = value
            cls.cls_providers[name] = value
        super(DeclarativeContainerMetaClass, cls).__setattr__(name, value)

    def __delattr__(cls, str name):
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

    provider_type = Provider
    """Type of providers that could be placed in container.

    :type: type
    """

    instance_type = DynamicContainer
    """Type of container that is returned on instantiating declarative
    container.

    :type: type
    """

    containers = dict()
    """Read-only dictionary of all nested containers.

    :type: dict[str, :py:class:`DeclarativeContainer`]
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

    __self__ = None
    """Provider that provides current container.

    :type: :py:class:`dependency_injector.providers.Provider`
    """

    def __new__(cls, **overriding_providers):
        """Constructor.

        :return: Dynamic container with copy of all providers.
        :rtype: :py:class:`DynamicContainer`
        """
        container = cls.instance_type()
        container.provider_type = cls.provider_type
        container.declarative_parent = cls
        container.set_providers(**deepcopy(cls.providers))
        container.override_providers(**overriding_providers)
        return container

    @classmethod
    def override(cls, object overriding):
        """Override current container by overriding container.

        :param overriding: Overriding container.
        :type overriding: :py:class:`DeclarativeContainer`

        :raise: :py:exc:`dependency_injector.errors.Error` if trying to
                override container by itself or its subclasses

        :rtype: None
        """
        if issubclass(cls, overriding):
            raise Error('Container {0} could not be overridden '
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
            raise Error('Container {0} is not overridden'.format(cls))

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

    @classmethod
    def resolve_provider_name(cls, provider_to_resolve):
        """Try to resolve provider name by its instance."""
        for provider_name, container_provider in cls.providers.items():
            if container_provider is provider_to_resolve:
                return provider_name
        else:
            return None


def override(object container):
    """:py:class:`DeclarativeContainer` overriding decorator.

    :param container: Container that should be overridden by decorated
                      container.
    :type container: :py:class:`DeclarativeContainer`

    :return: Declarative container's overriding decorator.
    :rtype: callable(:py:class:`DeclarativeContainer`)
    """
    def _decorator(object overriding_container):
        """Overriding decorator."""
        container.override(overriding_container)
        return overriding_container
    return _decorator


def copy(object container):
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
        cdef dict memo = dict()
        for name, provider in six.iteritems(copied_container.cls_providers):
            try:
                source_provider = getattr(container, name)
            except AttributeError:
                pass
            else:
                memo[id(source_provider)] = provider

        providers_copy = deepcopy(container.providers, memo)
        for name, provider in six.iteritems(providers_copy):
            setattr(copied_container, name, provider)

        return copied_container
    return _decorator


cpdef bint is_container(object instance):
    """Check if instance is container instance.

    :param instance: Instance to be checked.
    :type instance: object

    :rtype: bool
    """
    return getattr(instance, '__IS_CONTAINER__', False) is True


cpdef object _check_provider_type(object container, object provider):
    if not isinstance(provider, container.provider_type):
        raise Error('{0} can contain only {1} '
                    'instances'.format(container, container.provider_type))


cpdef bint _isawaitable(object instance):
    try:
        return <bint> inspect.isawaitable(instance)
    except AttributeError:
        return <bint> False
