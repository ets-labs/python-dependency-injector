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
        if hasattr(callback, '__injections__'):
            callback.__injections__ += (injection,)

        @wraps(callback)
        def decorated(*args, **kwargs):
            """Decorated with dependency injection callback."""
            for injection in getattr(decorated, '__injections__'):
                if injection.name not in kwargs:
                    kwargs[injection.name] = injection.value
            return callback(*args, **kwargs)

        setattr(decorated, '__injections__', (injection,))

        return decorated
    return decorator
