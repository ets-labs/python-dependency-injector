"""Utils module."""

from six import class_types

from .errors import Error


def is_provider(instance):
    """Check if instance is provider instance."""
    return (not isinstance(instance, class_types) and
            getattr(instance, '__IS_PROVIDER__', False) is True)


def ensure_is_provider(instance):
    """Check if instance is provider instance, otherwise raise and error."""
    if not is_provider(instance):
        raise Error('Expected provider instance, '
                    'got {0}'.format(str(instance)))
    return instance


def is_injection(instance):
    """Check if instance is injection instance."""
    return (not isinstance(instance, class_types) and
            getattr(instance, '__IS_INJECTION__', False) is True)


def ensure_is_injection(instance):
    """Check if instance is injection instance, otherwise raise and error."""
    if not is_injection(instance):
        raise Error('Expected injection instance, '
                    'got {0}'.format(str(instance)))
    return instance


def is_kwarg_injection(instance):
    """Check if instance is keyword argument injection instance."""
    return (not isinstance(instance, class_types) and
            getattr(instance, '__IS_KWARG_INJECTION__', False) is True)


def is_attribute_injection(instance):
    """Check if instance is attribute injection instance."""
    return (not isinstance(instance, class_types) and
            getattr(instance, '__IS_ATTRIBUTE_INJECTION__', False) is True)


def is_method_injection(instance):
    """Check if instance is method injection instance."""
    return (not isinstance(instance, class_types) and
            getattr(instance, '__IS_METHOD_INJECTION__', False) is True)


def get_injectable_kwargs(kwargs, injections):
    """Return dictionary of kwargs, patched with injections."""
    init_kwargs = dict(((injection.name, injection.value)
                        for injection in injections))
    init_kwargs.update(kwargs)
    return init_kwargs
