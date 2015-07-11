"""Injections module."""

from .utils import is_provider


class Injection(object):

    """Base injection class."""

    __IS_OBJECTS_INJECTION__ = True
    __slots__ = ('name', 'injectable', 'delegate')

    def __init__(self, name, injectable, delegate=False):
        """Initializer."""
        self.name = name
        self.injectable = injectable
        self.delegate = delegate

    @property
    def value(self):
        """Return injectable value."""
        if is_provider(self.injectable) and not self.delegate:
            return self.injectable()
        return self.injectable


class KwArg(Injection):

    """Keyword argument injection."""

    __IS_OBJECTS_KWARG_INJECTION__ = True


class Attribute(Injection):

    """Attribute injection."""

    __IS_OBJECTS_ATTRIBUTE_INJECTION__ = True


class Method(Injection):

    """Method injection."""

    __IS_OBJECTS_METHOD_INJECTION__ = True
