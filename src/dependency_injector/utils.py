"""Dependency injector utils module."""

import copy as _copy
import types
import threading

import six

from dependency_injector import errors


GLOBAL_LOCK = threading.RLock()
"""Dependency injector global reentrant lock.

:type: :py:class:`threading.RLock`
"""

if six.PY2:  # pragma: no cover
    _copy._deepcopy_dispatch[types.MethodType] = \
        lambda obj, memo: type(obj)(obj.im_func,
                                    _copy.deepcopy(obj.im_self, memo),
                                    obj.im_class)


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
        raise errors.Error('Expected provider instance, '
                           'got {0}'.format(str(instance)))
    return instance


def is_delegated(instance):
    """Check if instance is delegated provider.

    :param instance: Instance to be checked.
    :type instance: object

    :rtype: bool
    """
    return (not isinstance(instance, six.class_types) and
            hasattr(instance, '__IS_DELEGATED__') and
            getattr(instance, '__IS_DELEGATED__') is True)


def is_container(instance):
    """Check if instance is container instance.

    :param instance: Instance to be checked.
    :type instance: object

    :rtype: bool
    """
    return (hasattr(instance, '__IS_CONTAINER__') and
            getattr(instance, '__IS_CONTAINER__', False) is True)


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


def deepcopy(instance, memo=None):
    """Make full copy of instance."""
    return _copy.deepcopy(instance, memo)
