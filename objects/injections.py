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


def inject(injection):
    """
    Injection decorator.
    """
    def decorator(callback_or_cls):
        if isclass(callback_or_cls):
            cls = callback_or_cls
            if isinstance(injection, Attribute):
                setattr(cls, injection.name, injection.injectable)
            elif isinstance(injection, InitArg):
                cls.__init__ = decorator(cls.__init__)
            return cls
        else:
            callback = callback_or_cls

            @wraps(callback)
            def wrapped(*args, **kwargs):
                if injection.name not in kwargs:
                    kwargs[injection.name] = injection.value
                return callback(*args, **kwargs)
            return wrapped
    return decorator
