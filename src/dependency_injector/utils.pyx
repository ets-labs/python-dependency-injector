"""Dependency injector utils.

Powered by Cython.
"""

cimport cpython.version

from dependency_injector cimport errors

import copy as _copy
import types
import threading


GLOBAL_LOCK = threading.RLock()
"""Dependency injector global reentrant lock.

:type: :py:class:`threading.RLock`
"""

if cpython.version.PY_MAJOR_VERSION < 3:  # pragma: no cover
    CLASS_TYPES = (type, types.ClassType)

    _copy._deepcopy_dispatch[types.MethodType] = \
        lambda obj, memo: type(obj)(obj.im_func,
                                    _copy.deepcopy(obj.im_self, memo),
                                    obj.im_class)
else:  # pragma: no cover
    CLASS_TYPES = (type,)



cpdef bint is_provider(object instance):
    """Check if instance is provider instance.

    :param instance: Instance to be checked.
    :type instance: object

    :rtype: bool
    """
    return (not isinstance(instance, CLASS_TYPES) and
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
        raise errors.Error('Expected provider instance, '
                           'got {0}'.format(str(instance)))
    return instance


cpdef bint is_delegated(object instance):
    """Check if instance is delegated provider.

    :param instance: Instance to be checked.
    :type instance: object

    :rtype: bool
    """
    return (not isinstance(instance, CLASS_TYPES) and
            getattr(instance, '__IS_DELEGATED__', False) is True)


cpdef bint is_container(object instance):
    """Check if instance is container instance.

    :param instance: Instance to be checked.
    :type instance: object

    :rtype: bool
    """
    return getattr(instance, '__IS_CONTAINER__', False) is True


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


cpdef object deepcopy(object instance, dict memo=None):
    """Make full copy of instance."""
    return _copy.deepcopy(instance, memo)

