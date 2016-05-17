"""Injections module."""

import itertools

import six

from dependency_injector.utils import (
    is_provider,
    is_injection,
    is_arg_injection,
    is_kwarg_injection,
    is_delegated_provider,
    fetch_cls_init,
)

from dependency_injector.errors import Error


@six.python_2_unicode_compatible
class Injection(object):
    """Base injection class.

    All injections extend this class.

    .. py:attribute:: injectable

        Injectable value, could be provider or any other object.

        :type: object | :py:class:`dependency_injector.providers.Provider`

    .. py:attribute:: call_injectable

        Flag that is set to ``True`` if it is needed to call injectable.

        Injectable needs to be called if it is not delegated provider.

        :type: bool
    """

    __IS_INJECTION__ = True
    __slots__ = ('injectable', 'call_injectable')

    def __init__(self, injectable):
        """Initializer.

        :param injectable: Injectable value, could be provider or any
                           other object.
        :type injectable: object |
                          :py:class:`dependency_injector.providers.Provider`
        """
        self.injectable = injectable
        self.call_injectable = (is_provider(injectable) and
                                not is_delegated_provider(injectable))
        super(Injection, self).__init__()

    @property
    def value(self):
        """Read-only property that represents injectable value.

        Injectable values and delegated providers are provided "as is".
        Other providers will be called every time, when injection needs to
        be done.

        :rtype: object
        """
        if self.call_injectable:
            return self.injectable.provide()
        return self.injectable

    def __str__(self):
        """Return string representation of provider.

        :rtype: str
        """
        return '<{injection}({injectable}) at {address}>'.format(
            injection='.'.join((self.__class__.__module__,
                                self.__class__.__name__)),
            injectable=repr(self.injectable),
            address=hex(id(self)))

    __repr__ = __str__


class Arg(Injection):
    """Positional argument injection."""

    __IS_ARG_INJECTION__ = True


@six.python_2_unicode_compatible
class _NamedInjection(Injection):
    """Base class of named injections.

    .. py:attribute:: name

        Injection target's name (keyword argument, attribute).

        :type: str
    """

    __slots__ = ('name',)

    def __init__(self, name, injectable):
        """Initializer.

        :param name: Injection target's name.
        :type name: str

        :param injectable: Injectable value, could be provider or any
                           other object.
        :type injectable: object |
                          :py:class:`dependency_injector.providers.Provider`
        """
        self.name = name
        super(_NamedInjection, self).__init__(injectable)

    def __str__(self):
        """Return string representation of provider.

        :rtype: str
        """
        return '<{injection}({name}, {injectable}) at {address}>'.format(
            name=repr(self.name),
            injection='.'.join((self.__class__.__module__,
                                self.__class__.__name__)),
            injectable=repr(self.injectable),
            address=hex(id(self)))

    __repr__ = __str__


class KwArg(_NamedInjection):
    """Keyword argument injection.

    .. py:attribute:: name

        Keyword argument's name.

        :type: str
    """

    __IS_KWARG_INJECTION__ = True


class Attribute(_NamedInjection):
    """Attribute injection.

    .. py:attribute:: name

        Attribute's name.

        :type: str
    """

    __IS_ATTRIBUTE_INJECTION__ = True


def inject(*args, **kwargs):
    """Dependency injection decorator.

    :py:func:`inject` decorator can be used for making inline dependency
    injections. It patches decorated callable in such way that dependency
    injection will be done during every call of decorated callable.

    :py:func:`inject` decorator supports different syntaxes of passing
    injections:

    .. code-block:: python

        # Positional arguments injections (simplified syntax):
        @inject(1, 2)
        def some_function(arg1, arg2):
            pass

        # Keyword arguments injections (simplified syntax):
        @inject(arg1=1)
        @inject(arg2=2)
        def some_function(arg1, arg2):
            pass

        # Keyword arguments injections (extended (full) syntax):
        @inject(KwArg('arg1', 1))
        @inject(KwArg('arg2', 2))
        def some_function(arg1, arg2):
            pass

        # Keyword arguments injections into class init (simplified syntax):
        @inject(arg1=1)
        @inject(arg2=2)
        class SomeClass(object):

            def __init__(self, arg1, arg2):
                pass

    :param args: Tuple of context positional arguments.
    :type args: tuple[object]

    :param kwargs: Dictionary of context keyword arguments.
    :type kwargs: dict[str, object]

    :return: Class / callable decorator
    :rtype: (callable) -> (type | callable)
    """
    arg_injections = _parse_args_injections(args)
    kwarg_injections = _parse_kwargs_injections(args, kwargs)

    def decorator(callback_or_cls):
        """Dependency injection decorator."""
        if isinstance(callback_or_cls, six.class_types):
            cls = callback_or_cls
            cls_init = fetch_cls_init(cls)
            if not cls_init:
                raise Error(
                    'Class {0}.{1} has no __init__() '.format(cls.__module__,
                                                              cls.__name__) +
                    'method and could not be decorated with @inject decorator')
            cls.__init__ = decorator(cls_init)
            return cls

        callback = callback_or_cls

        if hasattr(callback, '__INJECT_DECORATED__'):
            callback.args += arg_injections
            callback.kwargs += kwarg_injections
            callback.injections += arg_injections + kwarg_injections
            return callback

        @six.wraps(callback)
        def decorated(*args, **kwargs):
            """Decorated with dependency injection callback."""
            if decorated.args:
                args = tuple(arg.value for arg in decorated.args) + args

            for kwarg in decorated.kwargs:
                if kwarg.name not in kwargs:
                    kwargs[kwarg.name] = kwarg.value

            return callback(*args, **kwargs)

        decorated.__INJECT_DECORATED__ = True
        decorated.origin = callback
        decorated.args = arg_injections
        decorated.kwargs = kwarg_injections
        decorated.injections = arg_injections + kwarg_injections

        return decorated
    return decorator


def _parse_args_injections(args):
    return tuple(Arg(arg) if not is_injection(arg) else arg
                 for arg in args
                 if not is_injection(arg) or is_arg_injection(arg))


def _parse_kwargs_injections(args, kwargs):
    kwarg_injections = tuple(injection
                             for injection in args
                             if is_kwarg_injection(injection))
    if kwargs:
        kwarg_injections += tuple(itertools.starmap(KwArg,
                                                    six.iteritems(kwargs)))
    return kwarg_injections


def _parse_attribute_injections(attributes):
    return tuple(itertools.starmap(Attribute, six.iteritems(attributes)))
