"""Injections module."""

import six

from .utils import is_provider
from .utils import ensure_is_injection
from .utils import get_injectable_kwargs

from .errors import Error


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

    def decorator(callback, cls=None):
        """Dependency injection decorator."""
        if isinstance(callback, six.class_types):
            cls = callback
            try:
                cls_init = six.get_unbound_function(getattr(cls, '__init__'))
            except AttributeError:
                raise Error(
                    'Class {0} has no __init__() '.format(cls.__module__,
                                                          cls.__name__) +
                    'method and could not be decorated with @inject decorator')
            cls.__init__ = decorator(cls_init)
            return cls

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
