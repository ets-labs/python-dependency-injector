"""Dependency injector provider utils.

Powered by Cython.
"""

import sys
import types

import threading

from dependency_injector.errors import Error

GLOBAL_LOCK = threading.RLock()
"""Global reentrant lock.

:type: :py:class:`threading.RLock`
"""

if sys.version_info[0] == 3:  # pragma: no cover
    _CLASS_TYPES = (type,)
else:  # pragma: no cover
    _CLASS_TYPES = (type, types.ClassType)


cpdef bint is_provider(object instance):
    """Check if instance is provider instance.

    :param instance: Instance to be checked.
    :type instance: object

    :rtype: bool
    """
    return (not isinstance(instance, _CLASS_TYPES) and
            getattr(instance, '__IS_PROVIDER__', False) is True)


cpdef object ensure_is_provider(object instance):
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


cpdef bint is_delegated(object instance):
    """Check if instance is delegated provider.

    :param instance: Instance to be checked.
    :type instance: object

    :rtype: bool
    """
    return (not isinstance(instance, _CLASS_TYPES) and
            getattr(instance, '__IS_DELEGATED__', False) is True)


cpdef str represent_provider(object provider, object provides):
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
