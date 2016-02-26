"""Providers module."""

import six

from .injections import _parse_args_injections
from .injections import _parse_kwargs_injections

from .utils import ensure_is_provider
from .utils import is_attribute_injection
from .utils import is_method_injection
from .utils import represent_provider
from .utils import GLOBAL_LOCK

from .errors import Error


@six.python_2_unicode_compatible
class Provider(object):
    """Base provider class.

    :py:class:`Provider` is callable (implements ``__call__`` method). Every
    call to provider object returns provided result, according to the providing
    strategy of particular provider. This ``callable`` functionality is a
    regular part of providers API and it should be the same for all provider's
    subclasses.

    Implementation of particular providing strategy should be done in
    :py:meth:`Provider._provide` of :py:class:`Provider` subclass. Current
    method is called every time when not overridden provider is called.

    :py:class:`Provider` implements provider overriding logic that should be
    also common for all providers:

    .. code-block:: python

        provider1 = Factory(SomeClass)
        provider2 = Factory(ChildSomeClass)

        provider1.override(provider2)

        some_instance = provider1()
        assert isinstance(some_instance, ChildSomeClass)

    Also :py:class:`Provider` implements helper function for creating its
    delegates:

    .. code-block:: python

        provider = Factory(object)
        delegate = provider.delegate()

        delegated = delegate()

        assert provider is delegated

    All providers should extend this class.

    .. py:attribute:: overridden_by

        Tuple of overriding providers, if any.

        :type: tuple[:py:class:`Provider`] | None
    """

    __IS_PROVIDER__ = True
    __OPTIMIZED_CALLS__ = True
    __slots__ = ('overridden_by', '__call__')

    def __init__(self):
        """Initializer."""
        self.overridden_by = None
        super(Provider, self).__init__()
        # Enable __call__() / _provide() optimization
        if self.__class__.__OPTIMIZED_CALLS__:
            self.__call__ = self._provide

    def _provide(self, *args, **kwargs):
        """Providing strategy implementation.

        Abstract protected method that implements providing strategy of
        particular provider. Current method is called every time when not
        overridden provider is called. Need to be overridden in subclasses.
        """
        raise NotImplementedError()

    def _call_last_overriding(self, *args, **kwargs):
        """Call last overriding provider and return result."""
        return self.last_overriding(*args, **kwargs)

    @property
    def is_overridden(self):
        """Read-only property that is set to ``True`` if provider is overridden.

        :rtype: bool
        """
        return bool(self.overridden_by)

    @property
    def last_overriding(self):
        """Read-only reference to the last overriding provider, if any.

        :type: :py:class:`Provider` | None
        """
        return self.overridden_by[-1] if self.overridden_by else None

    def override(self, provider):
        """Override provider with another provider.

        :param provider: Overriding provider.
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

        # Disable __call__() / _provide() optimization
        if self.__class__.__OPTIMIZED_CALLS__:
            self.__call__ = self._call_last_overriding

    def reset_last_overriding(self):
        """Reset last overriding provider.

        :raise: :py:exc:`dependency_injector.errors.Error` if provider is not
                overridden.

        :rtype: None
        """
        if not self.overridden_by:
            raise Error('Provider {0} is not overridden'.format(str(self)))
        self.overridden_by = self.overridden_by[:-1]

        if not self.is_overridden:
            # Enable __call__() / _provide() optimization
            if self.__class__.__OPTIMIZED_CALLS__:
                self.__call__ = self._provide

    def reset_override(self):
        """Reset all overriding providers.

        :rtype: None
        """
        self.overridden_by = None

        # Enable __call__() / _provide() optimization
        if self.__class__.__OPTIMIZED_CALLS__:
            self.__call__ = self._provide

    def delegate(self):
        """Return provider's delegate.

        :rtype: :py:class:`Delegate`
        """
        return Delegate(self)

    def __str__(self):
        """Return string representation of provider.

        :rtype: str
        """
        return represent_provider(provider=self, provides=None)

    __repr__ = __str__


@six.python_2_unicode_compatible
class Delegate(Provider):
    """:py:class:`Delegate` provider delegates another provider.

    .. code-block:: python

        provider = Factory(object)
        delegate = Delegate(provider)

        delegated = delegate()

        assert provider is delegated

    .. py:attribute:: delegated

        Delegated provider.

        :type: :py:class:`Provider`
    """

    __slots__ = ('delegated',)

    def __init__(self, delegated):
        """Initializer.

        :provider delegated: Delegated provider.
        :type delegated: :py:class:`Provider`
        """
        self.delegated = ensure_is_provider(delegated)
        super(Delegate, self).__init__()

    def _provide(self, *args, **kwargs):
        """Return provided instance.

        :param args: Tuple of context positional arguments.
        :type args: tuple[object]

        :param kwargs: Dictionary of context keyword arguments.
        :type kwargs: dict[str, object]

        :rtype: object
        """
        return self.delegated

    def __str__(self):
        """Return string representation of provider.

        :rtype: str
        """
        return represent_provider(provider=self, provides=self.delegated)

    __repr__ = __str__


@six.python_2_unicode_compatible
class Callable(Provider):
    """:py:class:`Callable` provider calls wrapped callable on every call.

    :py:class:`Callable` provider provides callable that is called on every
    provider call with some predefined dependency injections.

    :py:class:`Callable` syntax of passing injections is the same like
    :py:class:`Factory` one:

    .. code-block:: python

        # simplified syntax for passing positional and keyword argument
        # injections:
        some_function = Callable(some_function, 'arg1', 'arg2', arg3=3, arg4=4)

        # extended (full) syntax for passing positional and keyword argument
        # injections:
        some_function = Callable(some_function,
                                 injections.Arg(1),
                                 injections.Arg(2),
                                 injections.KwArg('some_arg', 3),
                                 injections.KwArg('other_arg', 4))

    .. py:attribute:: provides

        Provided callable.

        :type: callable

    .. py:attribute:: args

        Tuple of positional argument injections.

        :type: tuple[:py:class:`dependency_injector.injections.Arg`]

    .. py:attribute:: kwargs

        Tuple of keyword argument injections.

        :type: tuple[:py:class:`dependency_injector.injections.KwArg`]
    """

    __slots__ = ('provides', 'args', 'kwargs')

    def __init__(self, provides, *args, **kwargs):
        """Initializer.

        :param provides: Wrapped callable.
        :type provides: callable

        :param args: Tuple of injections.
        :type args: tuple

        :param kwargs: Dictionary of injections.
        :type kwargs: dict
        """
        if not callable(provides):
            raise Error('Provider {0} expected to get callable, '
                        'got {0}'.format('.'.join((self.__class__.__module__,
                                                   self.__class__.__name__)),
                                         provides))

        self.provides = provides

        self.args = _parse_args_injections(args)
        self.kwargs = _parse_kwargs_injections(args, kwargs)

        super(Callable, self).__init__()

    @property
    def injections(self):
        """Read-only tuple of all injections.

        :rtype: tuple[:py:class:`dependency_injector.injections.Injection`]
        """
        return self.args + self.kwargs

    def _provide(self, *args, **kwargs):
        """Return provided instance.

        :param args: Tuple of context positional arguments.
        :type args: tuple[object]

        :param kwargs: Dictionary of context keyword arguments.
        :type kwargs: dict[str, object]

        :rtype: object
        """
        if self.args:
            args = tuple(arg.value for arg in self.args) + args

        for kwarg in self.kwargs:
            if kwarg.name not in kwargs:
                kwargs[kwarg.name] = kwarg.value

        return self.provides(*args, **kwargs)

    def __str__(self):
        """Return string representation of provider.

        :rtype: str
        """
        return represent_provider(provider=self, provides=self.provides)

    __repr__ = __str__


class DelegatedCallable(Callable):
    """:py:class:`DelegatedCallable` is a delegated :py:class:`Callable`.

    :py:class:`DelegatedCallable` is a :py:class:`Callable`, that is injected
    "as is".

    .. py:attribute:: provides

        Provided callable.

        :type: callable

    .. py:attribute:: args

        Tuple of positional argument injections.

        :type: tuple[:py:class:`dependency_injector.injections.Arg`]

    .. py:attribute:: kwargs

        Tuple of keyword argument injections.

        :type: tuple[:py:class:`dependency_injector.injections.KwArg`]
    """

    __IS_DELEGATED__ = True


class Factory(Callable):
    """:py:class:`Factory` provider creates new instance on every call.

    :py:class:`Factory` supports different syntaxes of passing injections:

    .. code-block:: python

        # simplified syntax for passing positional and keyword argument
        # injections only:
        factory = Factory(SomeClass, 'arg1', 'arg2', arg3=3, arg4=4)

        # extended (full) syntax for passing any type of injections:
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

    .. py:attribute:: provided_type

        If provided type is defined, :py:class:`Factory` checks that
        :py:attr:`Factory.provides` is subclass of
        :py:attr:`Factory.provided_type`.

        :type: type | None

    .. py:attribute:: provides

        Class or other callable that provides object.

        :type: type | callable

    .. py:attribute:: args

        Tuple of positional argument injections.

        :type: tuple[:py:class:`dependency_injector.injections.Arg`]

    .. py:attribute:: kwargs

        Tuple of keyword argument injections.

        :type: tuple[:py:class:`dependency_injector.injections.KwArg`]

    .. py:attribute:: attributes

        Tuple of attribute injections.

        :type: tuple[:py:class:`dependency_injector.injections.Attribute`]

    .. py:attribute:: methods

        Tuple of method injections.

        :type: tuple[:py:class:`dependency_injector.injections.Method`]
    """

    provided_type = None

    __slots__ = ('attributes', 'methods')

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
        if (self.__class__.provided_type and
                not issubclass(provides, self.__class__.provided_type)):
            raise Error('{0} can provide only {1} instances'.format(
                self.__class__, self.__class__.provided_type))

        self.attributes = tuple(injection
                                for injection in args
                                if is_attribute_injection(injection))

        self.methods = tuple(injection
                             for injection in args
                             if is_method_injection(injection))

        super(Factory, self).__init__(provides, *args, **kwargs)

    @property
    def injections(self):
        """Read-only tuple of all injections.

        :rtype: tuple[:py:class:`dependency_injector.injections.Injection`]
        """
        return self.args + self.kwargs + self.attributes + self.methods

    def _provide(self, *args, **kwargs):
        """Return provided instance.

        :param args: Tuple of context positional arguments.
        :type args: tuple[object]

        :param kwargs: Dictionary of context keyword arguments.
        :type kwargs: dict[str, object]

        :rtype: object
        """
        if self.args:
            args = tuple(arg.value for arg in self.args) + args

        for kwarg in self.kwargs:
            if kwarg.name not in kwargs:
                kwargs[kwarg.name] = kwarg.value

        instance = self.provides(*args, **kwargs)

        for attribute in self.attributes:
            setattr(instance, attribute.name, attribute.value)
        for method in self.methods:
            getattr(instance, method.name)(method.value)

        return instance


class DelegatedFactory(Factory):
    """:py:class:`DelegatedFactory` is a delegated :py:class:`Factory`.

    :py:class:`DelegatedFactory` is a :py:class:`Factory`, that is injected
    "as is".

    .. py:attribute:: provided_type

        If provided type is defined, :py:class:`Factory` checks that
        :py:attr:`Factory.provides` is subclass of
        :py:attr:`Factory.provided_type`.

        :type: type | None

    .. py:attribute:: provides

        Class or other callable that provides object.

        :type: type | callable

    .. py:attribute:: args

        Tuple of positional argument injections.

        :type: tuple[:py:class:`dependency_injector.injections.Arg`]

    .. py:attribute:: kwargs

        Tuple of keyword argument injections.

        :type: tuple[:py:class:`dependency_injector.injections.KwArg`]

    .. py:attribute:: attributes

        Tuple of attribute injections.

        :type: tuple[:py:class:`dependency_injector.injections.Attribute`]

    .. py:attribute:: methods

        Tuple of method injections.

        :type: tuple[:py:class:`dependency_injector.injections.Method`]
    """

    __IS_DELEGATED__ = True


class Singleton(Factory):
    """:py:class:`Singleton` provider returns same instance on every call.

    :py:class:`Singleton` provider creates instance once and return it on every
    call. :py:class:`Singleton` extends :py:class:`Factory`, so, please follow
    :py:class:`Factory` documentation to go inside with injections syntax.

    :py:class:`Singleton` is thread-safe and could be used in multithreading
    environment without any negative impact.

    Retrieving of provided instance can be performed via calling
    :py:class:`Singleton` object:

    .. code-block:: python

        singleton = Singleton(SomeClass,
                              some_arg1=1,
                              some_arg2=2)
        some_object = singleton()

    .. py:attribute:: provided_type

        If provided type is defined, :py:class:`Factory` checks that
        :py:attr:`Factory.provides` is subclass of
        :py:attr:`Factory.provided_type`.

        :type: type | None

    .. py:attribute:: instance

        Read-only reference to singleton's instance.

        :type: object

    .. py:attribute:: provides

        Class or other callable that provides object.

        :type: type | callable

    .. py:attribute:: args

        Tuple of positional argument injections.

        :type: tuple[:py:class:`dependency_injector.injections.Arg`]

    .. py:attribute:: kwargs

        Tuple of keyword argument injections.

        :type: tuple[:py:class:`dependency_injector.injections.KwArg`]

    .. py:attribute:: attributes

        Tuple of attribute injections.

        :type: tuple[:py:class:`dependency_injector.injections.Attribute`]

    .. py:attribute:: methods

        Tuple of method injections.

        :type: tuple[:py:class:`dependency_injector.injections.Method`]
    """

    __slots__ = ('instance',)

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
        super(Singleton, self).__init__(provides, *args, **kwargs)

    def reset(self):
        """Reset cached instance, if any.

        :rtype: None
        """
        self.instance = None

    def _provide(self, *args, **kwargs):
        """Return provided instance.

        :param args: Tuple of context positional arguments.
        :type args: tuple[object]

        :param kwargs: Dictionary of context keyword arguments.
        :type kwargs: dict[str, object]

        :rtype: object
        """
        if self.instance:
            return self.instance

        with GLOBAL_LOCK:
            self.instance = super(Singleton, self)._provide(*args, **kwargs)

        return self.instance


class DelegatedSingleton(Singleton):
    """:py:class:`DelegatedSingleton` is a delegated :py:class:`Singleton`.

    :py:class:`DelegatedSingleton` is a :py:class:`Singleton`, that is injected
    "as is".

    .. py:attribute:: provided_type

        If provided type is defined, :py:class:`Factory` checks that
        :py:attr:`Factory.provides` is subclass of
        :py:attr:`Factory.provided_type`.

        :type: type | None

    .. py:attribute:: instance

        Read-only reference to singleton's instance.

        :type: object

    .. py:attribute:: provides

        Class or other callable that provides object.

        :type: type | callable

    .. py:attribute:: args

        Tuple of positional argument injections.

        :type: tuple[:py:class:`dependency_injector.injections.Arg`]

    .. py:attribute:: kwargs

        Tuple of keyword argument injections.

        :type: tuple[:py:class:`dependency_injector.injections.KwArg`]

    .. py:attribute:: attributes

        Tuple of attribute injections.

        :type: tuple[:py:class:`dependency_injector.injections.Attribute`]

    .. py:attribute:: methods

        Tuple of method injections.

        :type: tuple[:py:class:`dependency_injector.injections.Method`]
    """

    __IS_DELEGATED__ = True


@six.python_2_unicode_compatible
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

    .. py:attribute:: instance_of

        Class of required dependency.

        :type: type
    """

    __OPTIMIZED_CALLS__ = False
    __slots__ = ('instance_of',)

    def __init__(self, instance_of):
        """Initializer."""
        if not isinstance(instance_of, six.class_types):
            raise Error('ExternalDependency provider expects to get class, ' +
                        'got {0} instead'.format(str(instance_of)))
        self.instance_of = instance_of
        super(ExternalDependency, self).__init__()

    def __call__(self, *args, **kwargs):
        """Return provided instance.

        :param args: Tuple of context positional arguments.
        :type args: tuple[object]

        :param kwargs: Dictionary of context keyword arguments.
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

        :param provider: Provider that provides required dependency.
        :type provider: :py:class:`Provider`

        :rtype: None
        """
        return self.override(provider)

    def __str__(self):
        """Return string representation of provider.

        :rtype: str
        """
        return represent_provider(provider=self, provides=self.instance_of)

    __repr__ = __str__


@six.python_2_unicode_compatible
class Static(Provider):
    """:py:class:`Static` provider returns provided instance "as is".

    :py:class:`Static` provider is base implementation that provides exactly
    the same as it got on input.

    .. py:attribute:: provides

        Value that have to be provided.

        :type: object
    """

    __slots__ = ('provides',)

    def __init__(self, provides):
        """Initializer.

        :param provides: Value that have to be provided.
        :type provides: object
        """
        self.provides = provides
        super(Static, self).__init__()

    def _provide(self, *args, **kwargs):
        """Return provided instance.

        :param args: Tuple of context positional arguments.
        :type args: tuple[object]

        :param kwargs: Dictionary of context keyword arguments.
        :type kwargs: dict[str, object]

        :rtype: object
        """
        return self.provides

    def __str__(self):
        """Return string representation of provider.

        :rtype: str
        """
        return represent_provider(provider=self, provides=self.provides)

    __repr__ = __str__


StaticProvider = Static
# Backward compatibility for versions < 1.11.1


class Class(Static):
    """:py:class:`Class` returns provided class "as is".

    .. code-block:: python

        cls_provider = Class(object)
        object_cls = cls_provider()
    """


class Object(Static):
    """:py:class:`Object` returns provided object "as is".

    .. code-block:: python

        object_provider = Object(object())
        object_instance = object_provider()
    """


class Function(Static):
    """:py:class:`Function` returns provided function "as is".

    .. code-block:: python

        function_provider = Function(len)
        len_function = function_provider()
    """


class Value(Static):
    """:py:class:`Value` returns provided value "as is".

    .. code-block:: python

        value_provider = Value(31337)
        value = value_provider()
    """


@six.python_2_unicode_compatible
class Config(Provider):
    """:py:class:`Config` provider provide dict values.

    :py:class:`Config` provider creates :py:class:`ChildConfig` objects for all
    undefined attribute calls. It makes possible to create deferred config
    value providers. It might be useful in cases where it is needed to
    define / pass some configuration in declarative manner, while
    configuration values will be loaded / updated in application's runtime.
    """

    __slots__ = ('value',)

    def __init__(self, value=None):
        """Initializer.

        :param value: Configuration dictionary.
        :type value: dict[str, object]
        """
        if not value:
            value = dict()
        self.value = value
        super(Config, self).__init__()

    def __getattr__(self, item):
        """Return instance of deferred config.

        :param item: Name of configuration option or section.
        :type item: str

        :rtype: :py:class:`ChildConfig`
        """
        return ChildConfig(parents=(item,), root_config=self)

    def _provide(self, paths=None):
        """Return provided instance.

        :param paths: Tuple of pieces of configuration option / section path.
        :type args: tuple[str]

        :rtype: object
        """
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
        """Update current value from another one.

        :param value: Configuration dictionary.
        :type value: dict[str, object]

        :rtype: None
        """
        self.value.update(value)

    def __str__(self):
        """Return string representation of provider.

        :rtype: str
        """
        return represent_provider(provider=self, provides=self.value)

    __repr__ = __str__


@six.python_2_unicode_compatible
class ChildConfig(Provider):
    """:py:class:`ChildConfig` provider provides value from :py:class:`Config`.

    :py:class:`ChildConfig` provides value from the root config object
    according to the current path in the config tree.
    """

    __slots__ = ('parents', 'root_config')

    def __init__(self, parents, root_config):
        """Initializer.

        :param parents: Tuple of pieces of configuration option / section
            parent path.
        :type parents: tuple[str]

        :param root_config: Root configuration object.
        :type root_config: :py:class:`Config`
        """
        self.parents = parents
        self.root_config = root_config
        super(ChildConfig, self).__init__()

    def __getattr__(self, item):
        """Return instance of deferred config.

        :param item: Name of configuration option or section.
        :type item: str

        :rtype: :py:class:`ChildConfig`
        """
        return ChildConfig(parents=self.parents + (item,),
                           root_config=self.root_config)

    def _provide(self, *args, **kwargs):
        """Return provided instance.

        :param args: Tuple of context positional arguments.
        :type args: tuple[object]

        :param kwargs: Dictionary of context keyword arguments.
        :type kwargs: dict[str, object]

        :rtype: object
        """
        return self.root_config(self.parents)

    def __str__(self):
        """Return string representation of provider.

        :rtype: str
        """
        return represent_provider(provider=self,
                                  provides='.'.join(self.parents))

    __repr__ = __str__
