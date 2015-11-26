"""Utils module."""

import threading

import six

from .errors import Error


GLOBAL_LOCK = threading.RLock()
"""Dependency injector global reentrant lock.

:type: :py:class:`threading.RLock`
"""


def is_provider(instance):
    """Check if instance is provider instance.

    :param instance: Instance to be checked.
    :type instance: object

    :rtype: bool
    """
    return (not isinstance(instance, six.class_types) and
            hasattr(instance, '__IS_PROVIDER__') and
            getattr(instance, '__IS_PROVIDER__') is True)


def ensure_is_provider(instance):
    """Check if instance is provider instance and return it.

    :param instance: Instance to be checked.
    :type instance: object

    :raise: :py:exc:`dependency_injector.errors.Error` if provided instance is
            not provider.

    :rtype: :py:class:`dependency_injector.providers.Provider`
    """
    if not is_provider(instance):
        raise Error('Expected provider instance, '
                    'got {0}'.format(str(instance)))
    return instance


def is_injection(instance):
    """Check if instance is injection instance.

    :param instance: Instance to be checked.
    :type instance: object

    :rtype: bool
    """
    return (not isinstance(instance, six.class_types) and
            hasattr(instance, '__IS_INJECTION__') and
            getattr(instance, '__IS_INJECTION__') is True)


def ensure_is_injection(instance):
    """Check if instance is injection instance and return it.

    :param instance: Instance to be checked.
    :type instance: object

    :raise: :py:exc:`dependency_injector.errors.Error` if provided instance is
            not injection.

    :rtype: :py:class:`dependency_injector.injections.Injection`
    """
    if not is_injection(instance):
        raise Error('Expected injection instance, '
                    'got {0}'.format(str(instance)))
    return instance


def is_arg_injection(instance):
    """Check if instance is positional argument injection instance.

    :param instance: Instance to be checked.
    :type instance: object

    :rtype: bool
    """
    return (not isinstance(instance, six.class_types) and
            hasattr(instance, '__IS_ARG_INJECTION__') and
            getattr(instance, '__IS_ARG_INJECTION__', False) is True)


def is_kwarg_injection(instance):
    """Check if instance is keyword argument injection instance.

    :param instance: Instance to be checked.
    :type instance: object

    :rtype: bool
    """
    return (not isinstance(instance, six.class_types) and
            hasattr(instance, '__IS_KWARG_INJECTION__') and
            getattr(instance, '__IS_KWARG_INJECTION__', False) is True)


def is_attribute_injection(instance):
    """Check if instance is attribute injection instance.

    :param instance: Instance to be checked.
    :type instance: object

    :rtype: bool
    """
    return (not isinstance(instance, six.class_types) and
            hasattr(instance, '__IS_ATTRIBUTE_INJECTION__') and
            getattr(instance, '__IS_ATTRIBUTE_INJECTION__', False) is True)


def is_method_injection(instance):
    """Check if instance is method injection instance.

    :param instance: Instance to be checked.
    :type instance: object

    :rtype: bool
    """
    return (not isinstance(instance, six.class_types) and
            hasattr(instance, '__IS_METHOD_INJECTION__') and
            getattr(instance, '__IS_METHOD_INJECTION__', False) is True)


def is_catalog(instance):
    """Check if instance is catalog instance.

    :param instance: Instance to be checked.
    :type instance: object

    :rtype: bool
    """
    return (hasattr(instance, '__IS_CATALOG__') and
            getattr(instance, '__IS_CATALOG__', False) is True)


def is_dynamic_catalog(instance):
    """Check if instance is dynamic catalog instance.

    :param instance: Instance to be checked.
    :type instance: object

    :rtype: bool
    """
    return (not isinstance(instance, six.class_types) and is_catalog(instance))


def is_declarative_catalog(instance):
    """Check if instance is declarative catalog instance.

    :param instance: Instance to be checked.
    :type instance: object

    :rtype: bool
    """
    return (isinstance(instance, six.class_types) and is_catalog(instance))


def is_catalog_bundle(instance):
    """Check if instance is catalog bundle instance.

    :param instance: Instance to be checked.
    :type instance: object

    :rtype: bool
    """
    return (not isinstance(instance, six.class_types) and
            hasattr(instance, '__IS_CATALOG_BUNDLE__') and
            getattr(instance, '__IS_CATALOG_BUNDLE__', False) is True)


def ensure_is_catalog_bundle(instance):
    """Check if instance is catalog bundle instance and return it.

    :param instance: Instance to be checked.
    :type instance: object

    :raise: :py:exc:`dependency_injector.errors.Error` if provided instance
            is not catalog bundle.

    :rtype: :py:class:`dependency_injector.catalogs.CatalogBundle`
    """
    if not is_catalog_bundle(instance):
        raise Error('Expected catalog bundle instance, '
                    'got {0}'.format(str(instance)))
    return instance
