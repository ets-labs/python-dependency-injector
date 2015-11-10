"""Utils module."""

import threading

import six

from .errors import Error


GLOBAL_LOCK = threading.RLock()


def is_provider(instance):
    """Check if instance is provider instance."""
    return (not isinstance(instance, six.class_types) and
            hasattr(instance, '__IS_PROVIDER__') and
            getattr(instance, '__IS_PROVIDER__') is True)


def ensure_is_provider(instance):
    """Check if instance is provider instance and return it.

    :raise: Error if provided instance is not provider.
    """
    if not is_provider(instance):
        raise Error('Expected provider instance, '
                    'got {0}'.format(str(instance)))
    return instance


def is_injection(instance):
    """Check if instance is injection instance."""
    return (not isinstance(instance, six.class_types) and
            hasattr(instance, '__IS_INJECTION__') and
            getattr(instance, '__IS_INJECTION__') is True)


def ensure_is_injection(instance):
    """Check if instance is injection instance, otherwise raise and error."""
    if not is_injection(instance):
        raise Error('Expected injection instance, '
                    'got {0}'.format(str(instance)))
    return instance


def is_arg_injection(instance):
    """Check if instance is positional argument injection instance."""
    return (not isinstance(instance, six.class_types) and
            hasattr(instance, '__IS_ARG_INJECTION__') and
            getattr(instance, '__IS_ARG_INJECTION__', False) is True)


def is_kwarg_injection(instance):
    """Check if instance is keyword argument injection instance."""
    return (not isinstance(instance, six.class_types) and
            hasattr(instance, '__IS_KWARG_INJECTION__') and
            getattr(instance, '__IS_KWARG_INJECTION__', False) is True)


def is_attribute_injection(instance):
    """Check if instance is attribute injection instance."""
    return (not isinstance(instance, six.class_types) and
            hasattr(instance, '__IS_ATTRIBUTE_INJECTION__') and
            getattr(instance, '__IS_ATTRIBUTE_INJECTION__', False) is True)


def is_method_injection(instance):
    """Check if instance is method injection instance."""
    return (not isinstance(instance, six.class_types) and
            hasattr(instance, '__IS_METHOD_INJECTION__') and
            getattr(instance, '__IS_METHOD_INJECTION__', False) is True)


def is_catalog(instance):
    """Check if instance is catalog instance."""
    return (hasattr(instance, '__IS_CATALOG__') and
            getattr(instance, '__IS_CATALOG__', False) is True)


def is_dynamic_catalog(instance):
    """Check if instance is dynamic catalog instance."""
    return (not isinstance(instance, six.class_types) and is_catalog(instance))


def is_declarative_catalog(instance):
    """Check if instance is declarative catalog instance."""
    return (isinstance(instance, six.class_types) and is_catalog(instance))


def is_catalog_bundle(instance):
    """Check if instance is catalog bundle instance."""
    return (not isinstance(instance, six.class_types) and
            hasattr(instance, '__IS_CATALOG_BUNDLE__') and
            getattr(instance, '__IS_CATALOG_BUNDLE__', False) is True)


def ensure_is_catalog_bundle(instance):
    """Check if instance is catalog bundle instance and return it.

    :raise: Error if provided instance is not catalog bundle.
    """
    if not is_catalog_bundle(instance):
        raise Error('Expected catalog bundle instance, '
                    'got {0}'.format(str(instance)))
    return instance
