"""Utils module."""

from inspect import isclass

from .errors import Error


def is_provider(instance):
    """Check if instance is provider instance."""
    return (not isclass(instance) and
            hasattr(instance, '__IS_OBJECTS_PROVIDER__'))


def ensure_is_provider(instance):
    """Check if instance is provider instance, otherwise raise and error."""
    if not is_provider(instance):
        raise Error('Expected provider instance, '
                    'got {}'.format(str(instance)))
    return instance


def is_injection(instance):
    """Check if instance is injection instance."""
    return (not isclass(instance) and
            hasattr(instance, '__IS_OBJECTS_INJECTION__'))


def is_init_arg_injection(instance):
    """Check if instance is init arg injection instance."""
    return (not isclass(instance) and
            hasattr(instance, '__IS_OBJECTS_INIT_ARG_INJECTION__'))


def is_attribute_injection(instance):
    """Check if instance is attribute injection instance."""
    return (not isclass(instance) and
            hasattr(instance, '__IS_OBJECTS_ATTRIBUTE_INJECTION__'))


def is_method_injection(instance):
    """Check if instance is method injection instance."""
    return (not isclass(instance) and
            hasattr(instance, '__IS_OBJECTS_METHOD_INJECTION__'))
