"""Injections module."""

from .utils import is_provider
from .utils import ensure_is_injection


class Injection(object):

    """Base injection class."""

    __IS_OBJECTS_INJECTION__ = True
    __slots__ = ('__IS_OBJECTS_INJECTION__', 'name', 'injectable')

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

    __IS_OBJECTS_KWARG_INJECTION__ = True
    __slots__ = ('__IS_OBJECTS_KWARG_INJECTION__',)


class Attribute(Injection):

    """Attribute injection."""

    __IS_OBJECTS_ATTRIBUTE_INJECTION__ = True
    __slots__ = ('__IS_OBJECTS_ATTRIBUTE_INJECTION__',)


class Method(Injection):

    """Method injection."""

    __IS_OBJECTS_METHOD_INJECTION__ = True
    __slots__ = ('__IS_OBJECTS_METHOD_INJECTION__',)


def inject(injection):
    """Inject decorator.

    :type injection: Injection
    :return: (callable) -> (callable)
    """
    injection = ensure_is_injection(injection)

    def decorator(callback):
        """Decorator."""
        def decorated(*args, **kwargs):
            """Decorated."""
            if injection.name not in kwargs:
                kwargs[injection.name] = injection.value
            return callback(*args, **kwargs)
        return decorated
    return decorator
