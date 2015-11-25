"""Injections module."""

import sys
import itertools

import six

from .utils import is_provider
from .utils import is_injection
from .utils import is_arg_injection
from .utils import is_kwarg_injection

from .errors import Error


_IS_PYPY = '__pypy__' in sys.builtin_module_names
if _IS_PYPY or six.PY3:  # pragma: no cover
    _OBJECT_INIT = six.get_unbound_function(object.__init__)
else:  # pragma: no cover
    _OBJECT_INIT = None


class Injection(object):
    """Base injection class.

    All injections extend this class.
    """

    __IS_INJECTION__ = True
    __slots__ = ('injectable', 'is_provider')

    def __init__(self, injectable):
        """Initializer.

        :param injectable: Injectable value, could be provider or any
                           other object.
        :type injectable: object |
                          :py:class:`dependency_injector.providers.Provider`
        """
        self.injectable = injectable
        """Injectable value, could be provider or any other object.

        :type: object | :py:class:`dependency_injector.providers.Provider`
        """

        self.is_provider = is_provider(injectable)
        """Flag that is set to ``True`` if injectable value is provider.

        :type: bool
        """

        super(Injection, self).__init__()

    @property
    def value(self):
        """Read-only property that represents injectable value.

        Injectable values are provided "as is", except of providers
        (subclasses of :py:class:`dependency_injector.providers.Provider`).
        Providers will be called every time, when injection needs to be done.

        :rtype: object
        """
        if self.is_provider:
            return self.injectable()
        return self.injectable


class _NamedInjection(Injection):
    """Base class of named injections."""

    __slots__ = ('name',)

    def __init__(self, name, injectable):
        """Initializer."""
        self.name = name
        super(_NamedInjection, self).__init__(injectable)


class Arg(Injection):
    """Positional argument injection."""

    __IS_ARG_INJECTION__ = True


class KwArg(_NamedInjection):
    """Keyword argument injection."""

    __IS_KWARG_INJECTION__ = True


class Attribute(_NamedInjection):
    """Attribute injection."""

    __IS_ATTRIBUTE_INJECTION__ = True


class Method(_NamedInjection):
    """Method injection."""

    __IS_METHOD_INJECTION__ = True


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

    :return: Class / callable decorator
    :rtype: (callable) -> (type | callable)
    """
    arg_injections = _parse_args_injections(args)
    kwarg_injections = _parse_kwargs_injections(args, kwargs)

    def decorator(callback_or_cls):
        """Dependency injection decorator."""
        if isinstance(callback_or_cls, six.class_types):
            cls = callback_or_cls
            try:
                cls_init = six.get_unbound_function(cls.__init__)
                assert cls_init is not _OBJECT_INIT
            except (AttributeError, AssertionError):
                raise Error(
                    'Class {0}.{1} has no __init__() '.format(cls.__module__,
                                                              cls.__name__) +
                    'method and could not be decorated with @inject decorator')
            cls.__init__ = decorator(cls_init)
            return cls

        callback = callback_or_cls
        if hasattr(callback, 'injections'):
            callback.args += arg_injections
            callback.kwargs += kwarg_injections
            callback.injections += arg_injections + kwarg_injections
            return callback

        @six.wraps(callback)
        def decorated(*args, **kwargs):
            """Decorated with dependency injection callback."""
            return callback(*_get_injectable_args(args, decorated.args),
                            **_get_injectable_kwargs(kwargs, decorated.kwargs))

        decorated.args = arg_injections
        decorated.kwargs = kwarg_injections
        decorated.injections = arg_injections + kwarg_injections

        return decorated
    return decorator


def _parse_args_injections(args):
    """Parse positional argument injections according to current syntax."""
    return tuple(Arg(arg) if not is_injection(arg) else arg
                 for arg in args
                 if not is_injection(arg) or is_arg_injection(arg))


def _parse_kwargs_injections(args, kwargs):
    """Parse keyword argument injections according to current syntax."""
    kwarg_injections = tuple(injection
                             for injection in args
                             if is_kwarg_injection(injection))
    if kwargs:
        kwarg_injections += tuple(KwArg(name, value)
                                  for name, value in six.iteritems(kwargs))
    return kwarg_injections


def _get_injectable_args(context_args, arg_injections):
    """Return tuple of positional arguments, patched with injections."""
    return itertools.chain((arg.value for arg in arg_injections), context_args)


def _get_injectable_kwargs(context_kwargs, kwarg_injections):
    """Return dictionary of keyword arguments, patched with injections."""
    injectable_kwargs = dict((kwarg.name, kwarg.value)
                             for kwarg in kwarg_injections)
    injectable_kwargs.update(context_kwargs)
    return injectable_kwargs
