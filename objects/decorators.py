"""Decorators module."""

from six import wraps

from .utils import ensure_is_injection


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
            for injection in getattr(decorated, '_injections'):
                if injection.name not in kwargs:
                    kwargs[injection.name] = injection.value
            return callback(*args, **kwargs)

        setattr(decorated, '_injections', (injection,))

        return decorated
    return decorator
