"""Dependency injector creational providers."""

from dependency_injector.providers.callable import Callable
from dependency_injector.utils import (
    is_attribute_injection,
    GLOBAL_LOCK,
)
from dependency_injector.errors import Error


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

    .. py:attribute:: cls

        Class that provides object.
        Alias for :py:attr:`provides`.

        :type: type

    .. py:attribute:: args

        Tuple of positional argument injections.

        :type: tuple[:py:class:`dependency_injector.injections.Arg`]

    .. py:attribute:: kwargs

        Tuple of keyword argument injections.

        :type: tuple[:py:class:`dependency_injector.injections.KwArg`]

    .. py:attribute:: attributes

        Tuple of attribute injections.

        :type: tuple[:py:class:`dependency_injector.injections.Attribute`]
    """

    provided_type = None

    __slots__ = ('cls', 'attributes')

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

        self.attributes = tuple()

        super(Factory, self).__init__(provides, *args, **kwargs)

        self.cls = self.provides

    @property
    def injections(self):
        """Read-only tuple of all injections.

        :rtype: tuple[:py:class:`dependency_injector.injections.Injection`]
        """
        return self.args + self.kwargs + self.attributes

    def add_injections(self, *args, **kwargs):
        """Add provider injections.

        :param args: Tuple of injections.
        :type args: tuple

        :param kwargs: Dictionary of injections.
        :type kwargs: dict
        """
        self.attributes += tuple(injection
                                 for injection in args
                                 if is_attribute_injection(injection))

        super(Factory, self).add_injections(*args, **kwargs)
        return self

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

    .. py:attribute:: cls

        Class that provides object.
        Alias for :py:attr:`provides`.

        :type: type

    .. py:attribute:: args

        Tuple of positional argument injections.

        :type: tuple[:py:class:`dependency_injector.injections.Arg`]

    .. py:attribute:: kwargs

        Tuple of keyword argument injections.

        :type: tuple[:py:class:`dependency_injector.injections.KwArg`]

    .. py:attribute:: attributes

        Tuple of attribute injections.

        :type: tuple[:py:class:`dependency_injector.injections.Attribute`]
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

    .. py:attribute:: cls

        Class that provides object.
        Alias for :py:attr:`provides`.

        :type: type

    .. py:attribute:: args

        Tuple of positional argument injections.

        :type: tuple[:py:class:`dependency_injector.injections.Arg`]

    .. py:attribute:: kwargs

        Tuple of keyword argument injections.

        :type: tuple[:py:class:`dependency_injector.injections.KwArg`]

    .. py:attribute:: attributes

        Tuple of attribute injections.

        :type: tuple[:py:class:`dependency_injector.injections.Attribute`]
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

    .. py:attribute:: cls

        Class that provides object.
        Alias for :py:attr:`provides`.

        :type: type

    .. py:attribute:: args

        Tuple of positional argument injections.

        :type: tuple[:py:class:`dependency_injector.injections.Arg`]

    .. py:attribute:: kwargs

        Tuple of keyword argument injections.

        :type: tuple[:py:class:`dependency_injector.injections.KwArg`]

    .. py:attribute:: attributes

        Tuple of attribute injections.

        :type: tuple[:py:class:`dependency_injector.injections.Attribute`]
    """

    __IS_DELEGATED__ = True
