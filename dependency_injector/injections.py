"""Injections module."""

import sys
import itertools

import six

from .utils import is_provider
from .utils import is_injection
from .utils import is_arg_injection
from .utils import is_kwarg_injection

from .errors import Error


IS_PYPY = '__pypy__' in sys.builtin_module_names
if IS_PYPY or six.PY3:  # pragma: no cover
    OBJECT_INIT = six.get_unbound_function(object.__init__)
else:  # pragma: no cover
    OBJECT_INIT = None


class Injection(object):
    """Base injection class."""

    __IS_INJECTION__ = True
    __slots__ = ('injectable', 'is_provider')

    def __init__(self, injectable):
        """Initializer."""
        self.injectable = injectable
        self.is_provider = is_provider(injectable)

    @property
    def value(self):
        """Return injectable value."""
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

    :return: (callable) -> (callable)
    """
    arg_injections = _parse_args_injections(args)
    kwarg_injections = _parse_kwargs_injections(args, kwargs)

    def decorator(callback_or_cls):
        """Dependency injection decorator."""
        if isinstance(callback_or_cls, six.class_types):
            cls = callback_or_cls
            try:
                cls_init = six.get_unbound_function(cls.__init__)
                assert cls_init is not OBJECT_INIT
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
