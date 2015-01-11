"""
Injections module.
"""

from inspect import isclass
from functools import wraps


class Injection(object):
    """
    Base injection class.
    """

    def __init__(self, name, injectable):
        """
        Initializer.
        """
        self.name = name
        self.injectable = injectable

    @property
    def value(self):
        """
        Returns injectable value.
        """
        if hasattr(self.injectable, '__is_objects_provider__'):
            return self.injectable()
        return self.injectable


class InitArg(Injection):
    """
    Init argument injection.
    """


class Attribute(Injection):
    """
    Attribute injection.
    """


class Method(Injection):
    """
    Method injection.
    """


def uses(provider):
    """
    Providers usage decorator.
    """
    def decorator(cls):
        catalog = getattr(cls, 'catalog')
        # catalog.__add__provider__(provider)
        return cls
    return decorator
