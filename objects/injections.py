"""Injections module."""

from .utils import is_provider


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


class InitArg(Injection):

    """Init argument injection."""

    __IS_OBJECTS_INIT_ARG_INJECTION__ = True
    __slots__ = ('__IS_OBJECTS_INIT_ARG_INJECTION__',)


class Attribute(Injection):

    """Attribute injection."""

    __IS_OBJECTS_ATTRIBUTE_INJECTION__ = True
    __slots__ = ('__IS_OBJECTS_ATTRIBUTE_INJECTION__',)


class Method(Injection):

    """Method injection."""

    __IS_OBJECTS_METHOD_INJECTION__ = True
    __slots__ = ('__IS_OBJECTS_METHOD_INJECTION__',)
