"""Utils module."""

import sys
import threading

import six

from dependency_injector.errors import Error


GLOBAL_LOCK = threading.RLock()
"""Dependency injector global reentrant lock.

:type: :py:class:`threading.RLock`
"""

_IS_PYPY = '__pypy__' in sys.builtin_module_names
if _IS_PYPY or six.PY3:  # pragma: no cover
    _OBJECT_INIT = six.get_unbound_function(object.__init__)
else:  # pragma: no cover
    _OBJECT_INIT = None


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


def is_delegated_provider(instance):
    """Check if instance is delegated provider instance.

    :param instance: Instance to be checked.
    :type instance: object

    :rtype: bool
    """
    return (is_provider(instance) and
            hasattr(instance, '__IS_DELEGATED__') and
            getattr(instance, '__IS_DELEGATED__') is True)


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


def represent_provider(provider, provides):
    """Return string representation of provider.

    :param provider: Provider object
    :type provider: :py:class:`dependency_injector.providers.Provider`

    :param provides: Object that provider provides
    :type provider: object

    :return: String representation of provider
    :rtype: str
    """
    return '<{provider}({provides}) at {address}>'.format(
        provider='.'.join((provider.__class__.__module__,
                           provider.__class__.__name__)),
        provides=repr(provides) if provides is not None else '',
        address=hex(id(provider)))


def fetch_cls_init(cls):
    """Return reference to the class.__init__() method if it is defined.

    :param cls: Class instance
    :type cls: type

    :return: Reference to the class.__init__() if any, or None otherwise.
    :rtype: unbound method | None
    """
    try:
        cls_init = six.get_unbound_function(cls.__init__)
        assert cls_init is not _OBJECT_INIT
    except (AttributeError, AssertionError):
        return None
    else:
        return cls_init
