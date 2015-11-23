"""Providers module."""

import six

from .injections import _parse_args_injections
from .injections import _parse_kwargs_injections
from .injections import _get_injectable_args
from .injections import _get_injectable_kwargs

from .utils import ensure_is_provider
from .utils import is_attribute_injection
from .utils import is_method_injection
from .utils import GLOBAL_LOCK

from .errors import Error


class Provider(object):
    """Base provider class.

    :py:class:`Provider` is callable (implements ``__call__`` method). Every
    call to provider object returns provided result, according to the providing
    strategy of particular provider. This ``callable`` functionality is a
    regular part of providers API and it should be the same for all provider's
    subclasses.

    :py:class:`Provider` implements provider overriding logic that should be
    also common for all providers.

    Implementation of particular providing strategy should be done in
    :py:meth:`Provider._provide` of :py:class:`Provider` subclass. Current
    method is called every time when not overridden provider is called.

    All providers should extend this class.
    """

    __IS_PROVIDER__ = True
    __slots__ = ('overridden_by',)

    def __init__(self):
        """Initializer."""
        self.overridden_by = None

    def __call__(self, *args, **kwargs):
        """Return provided instance.

        Implementation of current method adds ``callable`` functionality for
        providers API and it should be common for all provider's subclasses.
        Also this method implements provider overriding logic that is also
        common for all providers. Implementation of particular providing
        strategy should be done in :py:meth:`Provider._provide` of
        :py:class:`Provider` subclass.
        """
        if self.overridden_by:
            return self.last_overriding(*args, **kwargs)
        return self._provide(*args, **kwargs)

    def _provide(self, *args, **kwargs):
        """Providing strategy implementation.

        Abstract protected method that implements providing strategy of
        particular provider. Current method is called every time when not
        overridden provider is called. Need to be overridden in subclasses.
        """
        raise NotImplementedError()

    @property
    def is_overridden(self):
        """Read-only property that is set to ``True`` if provider is overridden.

        :rtype: bool
        """
        return bool(self.overridden_by)

    @property
    def last_overriding(self):
        """Read-only reference to the last overriding provider, if any.

        :type: :py:class:`Provider`
        """
        try:
            return self.overridden_by[-1]
        except (TypeError, IndexError):
            raise Error('Provider {0} is not overridden'.format(str(self)))

    def override(self, provider):
        """Override provider with another provider.

        :param provider: overriding provider
        :type provider: :py:class:`Provider`

        :raise: :py:exc:`dependency_injector.errors.Error`
        """
        if provider is self:
            raise Error('Provider {0} could not be overridden '
                        'with itself'.format(self))
        if not self.is_overridden:
            self.overridden_by = (ensure_is_provider(provider),)
        else:
            self.overridden_by += (ensure_is_provider(provider),)

    def reset_last_overriding(self):
        """Reset last overriding provider.

        :rtype: None
        """
        if not self.is_overridden:
            raise Error('Provider {0} is not overridden'.format(str(self)))
        self.overridden_by = self.overridden_by[:-1]

    def reset_override(self):
        """Reset all overriding providers.

        :rtype: None
        """
        self.overridden_by = None

    def delegate(self):
        """Return provider's delegate.

        :rtype: :py:class:`Delegate`
        """
        return Delegate(self)


class Delegate(Provider):
    """Provider's delegate."""

    __slots__ = ('delegated',)

    def __init__(self, delegated):
        """Initializer.

        :provider delegated: Delegated provider
        :type delegated: :py:class:`Provider`
        """
        self.delegated = ensure_is_provider(delegated)
        super(Delegate, self).__init__()

    def _provide(self, *args, **kwargs):
        """Return provided instance.

        :param args: tuple of context positional arguments
        :type args: tuple[object]

        :param kwargs: dictionary of context keyword arguments
        :type kwargs: dict[str, object]

        :rtype: object
        """
        return self.delegated


class Factory(Provider):
    """:py:class:`Factory` provider creates new instance on every call.

    :py:class:`Factory` supports different syntaxes of passing injections:

    + simplified one syntax for passing positional and keyword argument
      injections only:

    .. code-block:: python

        factory = Factory(SomeClass, 'arg1', 'arg2', arg3=3, arg4=4)

    - extended (full) one syntax for passing any type of injections:

    .. code-block:: python

        factory = Factory(SomeClass,
                          injections.Arg(1),
                          injections.Arg(2),
                          injections.KwArg('some_arg', 3),
                          injections.KwArg('other_arg', 4),
                          injections.Attribute('some_attribute', 5))

    Retrieving of provided instance can be performed via calling
    :py:class:`Factory` object:

    .. code-block:: python

        factory = Factory(SomeClass,
                          some_arg1=1,
                          some_arg2=2)
        some_object = factory()
    """

    __slots__ = ('provides', 'args', 'kwargs', 'attributes', 'methods')

    def __init__(self, provides, *args, **kwargs):
        """Initializer.

        :param provides: Class or other callable that provides object
            for creation.
        :type provides: type | callable

        :param args: Tuple of injections.
        :type args: tuple

        :param kwargs: Dictionary of injections.
        :type kwargs: dict
        """
        if not callable(provides):
            raise Error('Factory provider expects to get callable, ' +
                        'got {0} instead'.format(str(provides)))
        self.provides = provides
        """Class or other callable that provides object for creation.

        :type: type | callable
        """

        self.args = _parse_args_injections(args)
        """Tuple of positional argument injections.

        :type: tuple[:py:class:`dependency_injector.injections.Arg`]
        """

        self.kwargs = _parse_kwargs_injections(args, kwargs)
        """Tuple of keyword argument injections.

        :type: tuple[:py:class:`dependency_injector.injections.KwArg`]
        """

        self.attributes = tuple(injection
                                for injection in args
                                if is_attribute_injection(injection))
        """Tuple of attribute injections.

        :type: tuple[:py:class:`dependency_injector.injections.Attribute`]
        """

        self.methods = tuple(injection
                             for injection in args
                             if is_method_injection(injection))
        """Tuple of method injections.

        :type: tuple[:py:class:`dependency_injector.injections.Method`]
        """

        super(Factory, self).__init__()

    @property
    def injections(self):
        """Read-only tuple of all injections.

        :rtype: tuple[:py:class:`dependency_injector.injections.Injection`]
        """
        return self.args + self.kwargs + self.attributes + self.methods

    def _provide(self, *args, **kwargs):
        """Return provided instance.

        :param args: tuple of context positional arguments
        :type args: tuple[object]

        :param kwargs: dictionary of context keyword arguments
        :type kwargs: dict[str, object]

        :rtype: object
        """
        instance = self.provides(*_get_injectable_args(args, self.args),
                                 **_get_injectable_kwargs(kwargs, self.kwargs))
        for attribute in self.attributes:
            setattr(instance, attribute.name, attribute.value)
        for method in self.methods:
            getattr(instance, method.name)(method.value)

        return instance


class Singleton(Provider):
    """:py:class:`Singleton` provider returns same instance on every call.

    :py:class:`Singleton` provider creates instance once and return it on every
    call. :py:class:`Singleton` uses :py:class:`Factory` for creation of
    instance, so, please follow :py:class:`Factory` documentation to go inside
    with injections syntax.

    :py:class:`Singleton` is thread-safe and could be used in multithreading
    environment without any negative impact.

    Retrieving of provided instance can be performed via calling
    :py:class:`Singleton` object:

    .. code-block:: python

        singleton = Singleton(SomeClass,
                              some_arg1=1,
                              some_arg2=2)
        some_object = singleton()

    """

    __slots__ = ('instance', 'factory')

    def __init__(self, provides, *args, **kwargs):
        """Initializer.

        :param provides: Class or other callable that provides object
            for creation.
        :type provides: type | callable

        :param args: Tuple of injections.
        :type args: tuple

        :param kwargs: Dictionary of injections.
        :type kwargs: dict
        """
        self.instance = None
        """Read-only reference to singleton's instance.

        :type: object
        """

        self.factory = Factory(provides, *args, **kwargs)
        """Singleton's factory object.

        :type: :py:class:`Factory`
        """

        super(Singleton, self).__init__()

    @property
    def provides(self):
        """Class or other callable that provides object for creation.

        :type: type | callable
        """
        return self.factory.provides

    @property
    def args(self):
        """Tuple of positional argument injections.

        :type: tuple[:py:class:`dependency_injector.injections.Arg`]
        """
        return self.factory.args

    @property
    def kwargs(self):
        """Tuple of keyword argument injections.

        :type: tuple[:py:class:`dependency_injector.injections.KwArg`]
        """
        return self.factory.kwargs

    @property
    def attributes(self):
        """Tuple of attribute injections.

        :type: tuple[:py:class:`dependency_injector.injections.Attribute`]
        """
        return self.factory.attributes

    @property
    def methods(self):
        """Tuple of method injections.

        :type: tuple[:py:class:`dependency_injector.injections.Method`]
        """
        return self.factory.methods

    @property
    def injections(self):
        """Read-only tuple of all injections.

        :rtype: tuple[:py:class:`dependency_injector.injections.Injection`]
        """
        return self.factory.injections

    def reset(self):
        """Reset cached instance, if any.

        :rtype: None
        """
        self.instance = None

    def _provide(self, *args, **kwargs):
        """Return provided instance.

        :param args: tuple of context positional arguments
        :type args: tuple[object]

        :param kwargs: dictionary of context keyword arguments
        :type kwargs: dict[str, object]

        :rtype: object
        """
        with GLOBAL_LOCK:
            if not self.instance:
                self.instance = self.factory(*args, **kwargs)
        return self.instance


class ExternalDependency(Provider):
    """:py:class:`ExternalDependency` provider describes dependency interface.

    This provider is used for description of dependency interface. That might
    be useful when dependency could be provided in the client's code only,
    but it's interface is known. Such situations could happen when required
    dependency has non-determenistic list of dependencies itself.

    .. code-block:: python

        database_provider = ExternalDependency(sqlite3.dbapi2.Connection)
        database_provider.override(Factory(sqlite3.connect, ':memory:'))

        database = database_provider()
    """

    __slots__ = ('instance_of',)

    def __init__(self, instance_of):
        """Initializer."""
        if not isinstance(instance_of, six.class_types):
            raise Error('ExternalDependency provider expects to get class, ' +
                        'got {0} instead'.format(str(instance_of)))
        self.instance_of = instance_of
        """Class of required dependency.

        :type: type
        """
        super(ExternalDependency, self).__init__()

    def __call__(self, *args, **kwargs):
        """Return provided instance.

        :param args: tuple of context positional arguments
        :type args: tuple[object]

        :param kwargs: dictionary of context keyword arguments
        :type kwargs: dict[str, object]

        :raise: :py:exc:`dependency_injector.errors.Error`

        :rtype: object
        """
        if not self.is_overridden:
            raise Error('Dependency is not defined')

        instance = self.last_overriding(*args, **kwargs)

        if not isinstance(instance, self.instance_of):
            raise Error('{0} is not an '.format(instance) +
                        'instance of {0}'.format(self.instance_of))

        return instance

    def provided_by(self, provider):
        """Set external dependency provider.

        :param provider: Provider that provides required dependency
        :type provider: :py:class:`Provider`

        :rtype: None
        """
        return self.override(provider)


class StaticProvider(Provider):
    """:py:class:`StaticProvider` returns provided instance "as is".

    :py:class:`StaticProvider` is base implementation that provides exactly
    the same as it got on input.
    """

    __slots__ = ('provides',)

    def __init__(self, provides):
        """Initializer.

        :param provides: Value that have to be provided.
        :type provides: object
        """
        self.provides = provides
        """Value that have to be provided.

        :type: object
        """
        super(StaticProvider, self).__init__()

    def _provide(self, *args, **kwargs):
        """Return provided instance.

        :param args: tuple of context positional arguments
        :type args: tuple[object]

        :param kwargs: dictionary of context keyword arguments
        :type kwargs: dict[str, object]

        :rtype: object
        """
        return self.provides


class Class(StaticProvider):
    """:py:class:`Class` returns provided class "as is".

    .. code-block:: python

        cls_provider = Class(object)
        object_cls = cls_provider()
    """


class Object(StaticProvider):
    """:py:class:`Object` returns provided object "as is".

    .. code-block:: python

        object_provider = Object(object())
        object_instance = object_provider()
    """


class Function(StaticProvider):
    """:py:class:`Function` returns provided function "as is".

    .. code-block:: python

        function_provider = Function(len)
        len_function = function_provider()
    """


class Value(StaticProvider):
    """:py:class:`Value` returns provided value "as is".

    .. code-block:: python

        value_provider = Value(31337)
        value = value_provider()
    """


class Callable(Provider):
    """:py:class:`Callable` provider calls wrapped callable on every call.

    :py:class:`Callable` provider provides callable that is called on every
    provider call with some predefined dependency injections.

    :py:class:`Callable` syntax of passing injections is the same like
    :py:class:`Factory` one:

    .. code-block:: python

        some_function = Callable(some_function, 'arg1', 'arg2', arg3=3, arg4=4)
        result = some_function()
    """

    __slots__ = ('callback', 'args', 'kwargs')

    def __init__(self, callback, *args, **kwargs):
        """Initializer.

        :param callback: Wrapped callable.
        :type callback: callable

        :param args: Tuple of injections.
        :type args: tuple

        :param kwargs: Dictionary of injections.
        :type kwargs: dict
        """
        if not callable(callback):
            raise Error('Callable expected, got {0}'.format(str(callback)))
        self.callback = callback
        """Wrapped callable.

        :type: callable
        """

        self.args = _parse_args_injections(args)
        """Tuple of positional argument injections.

        :type: tuple[:py:class:`dependency_injector.injections.Arg`]
        """

        self.kwargs = _parse_kwargs_injections(args, kwargs)
        """Tuple of keyword argument injections.

        :type: tuple[:py:class:`dependency_injector.injections.KwArg`]
        """

        super(Callable, self).__init__()

    @property
    def injections(self):
        """Read-only tuple of all injections.

        :rtype: tuple[:py:class:`dependency_injector.injections.Injection`]
        """
        return self.args + self.kwargs

    def _provide(self, *args, **kwargs):
        """Return provided instance.

        :param args: tuple of context positional arguments
        :type args: tuple[object]

        :param kwargs: dictionary of context keyword arguments
        :type kwargs: dict[str, object]

        :rtype: object
        """
        return self.callback(*_get_injectable_args(args, self.args),
                             **_get_injectable_kwargs(kwargs, self.kwargs))


class Config(Provider):
    """Config provider.

    Config provider provides dict values. Also config provider creates
    child config objects for all undefined attribute calls. It makes possible
    to create deferred config value provider.
    """

    __slots__ = ('value',)

    def __init__(self, value=None):
        """Initializer."""
        if not value:
            value = dict()
        self.value = value
        super(Config, self).__init__()

    def __getattr__(self, item):
        """Return instance of deferred config."""
        return ChildConfig(parents=(item,), root_config=self)

    def _provide(self, paths=None):
        """Return provided instance."""
        value = self.value
        if paths:
            for path in paths:
                try:
                    value = value[path]
                except KeyError:
                    raise Error('Config key '
                                '"{0}" is undefined'.format('.'.join(paths)))
        return value

    def update_from(self, value):
        """Update current value from another one."""
        self.value.update(value)


class ChildConfig(Provider):
    """Child config provider.

    Child config provide an value from the root config object according to
    the current path in the config tree.
    """

    __slots__ = ('parents', 'root_config')

    def __init__(self, parents, root_config):
        """Initializer."""
        self.parents = parents
        self.root_config = root_config
        super(ChildConfig, self).__init__()

    def __getattr__(self, item):
        """Return instance of deferred config."""
        return ChildConfig(parents=self.parents + (item,),
                           root_config=self.root_config)

    def _provide(self, *args, **kwargs):
        """Return provided instance."""
        return self.root_config(self.parents)
