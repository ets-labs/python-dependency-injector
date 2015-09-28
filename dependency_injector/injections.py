"""Injections module."""

import sys
import six

from .utils import is_provider
from .utils import ensure_is_injection
from .utils import get_injectable_kwargs

from .errors import Error


IS_PYPY = '__pypy__' in sys.builtin_module_names
if IS_PYPY or six.PY3:  # pragma: no cover
    OBJECT_INIT = six.get_unbound_function(object.__init__)
else:  # pragma: no cover
    OBJECT_INIT = None


class Injection(object):

    """Base injection class."""

    __IS_INJECTION__ = True
    __slots__ = ('name', 'injectable')

    def __init__(self, name, injectable):
        """Initializer."""
        self.name = name
        self.injectable = injectable

    @property
    def value(self):
        """Return injectable value."""
        if is_provider(self.injectable):
            return self.injectable()
        return self.injectable


class KwArg(Injection):

    """Keyword argument injection."""

    __IS_KWARG_INJECTION__ = True


class Attribute(Injection):

    """Attribute injection."""

    __IS_ATTRIBUTE_INJECTION__ = True


class Method(Injection):

    """Method injection."""

    __IS_METHOD_INJECTION__ = True


def inject(*args, **kwargs):
    """Dependency injection decorator.

    :type injection: Injection
    :return: (callable) -> (callable)
    """
    injections = tuple(KwArg(name, value)
                       for name, value in six.iteritems(kwargs))
    if args:
        injections += tuple(ensure_is_injection(injection)
                            for injection in args)

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
            callback.injections += injections
            return callback

        @six.wraps(callback)
        def decorated(*args, **kwargs):
            """Decorated with dependency injection callback."""
            return callback(*args,
                            **get_injectable_kwargs(kwargs,
                                                    decorated.injections))

        decorated.injections = injections

        return decorated
    return decorator
