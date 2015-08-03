"""Injections module."""

from six import wraps

from .utils import is_provider
from .utils import ensure_is_injection
from .utils import get_injectable_kwargs


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


def inject(injection):
    """Dependency injection decorator.

    :type injection: Injection
    :return: (callable) -> (callable)
    """
    injection = ensure_is_injection(injection)

    def decorator(callback):
        """Dependency injection decorator."""
        if hasattr(callback, '_injections'):
            callback._injections += (injection,)

        @wraps(callback)
        def decorated(*args, **kwargs):
            """Decorated with dependency injection callback."""
            return callback(*args,
                            **get_injectable_kwargs(kwargs,
                                                    getattr(decorated,
                                                            '_injections')))

        setattr(decorated, '_injections', (injection,))

        return decorated
    return decorator
