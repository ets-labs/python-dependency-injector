"""Decorators module."""

from six import wraps

from .utils import ensure_is_injection
from .utils import get_injectable_kwargs


def override(catalog):
    """Catalog overriding decorator."""
    def decorator(overriding_catalog):
        """Overriding decorator."""
        catalog.override(overriding_catalog)
        return overriding_catalog
    return decorator


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
