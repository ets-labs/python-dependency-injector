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
    """Inject decorator.

    :type injection: Injection
    :return: (callable) -> (callable)
    """
    injection = ensure_is_injection(injection)

    def decorator(callback):
        """Decorator."""
        @wraps(callback)
        def decorated(*args, **kwargs):
            """Decorated."""
            if injection.name not in kwargs:
                kwargs[injection.name] = injection.value
            return callback(*args, **kwargs)
        return decorated
    return decorator
