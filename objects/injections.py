"""Injections module."""


class Injection(object):

    """Base injection class."""

    def __init__(self, name, injectable):
        """Initializer."""
        self.name = name
        self.injectable = injectable

    @property
    def value(self):
        """Return injectable value."""
        if hasattr(self.injectable, '__is_objects_provider__'):
            return self.injectable()
        return self.injectable


class InitArg(Injection):

    """Init argument injection."""


class Attribute(Injection):

    """Attribute injection."""


class Method(Injection):

    """Method injection."""
