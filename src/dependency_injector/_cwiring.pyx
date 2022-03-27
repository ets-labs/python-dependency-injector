"""Wiring optimizations module."""

import copy
import functools
import sys
import types

from . import providers


if sys.version_info[0] == 3:  # pragma: no cover
    CLASS_TYPES = (type,)
else:  # pragma: no cover
    CLASS_TYPES = (type, types.ClassType)

    copy._deepcopy_dispatch[types.MethodType] = \
        lambda obj, memo: type(obj)(obj.im_func,
                                    copy.deepcopy(obj.im_self, memo),
                                    obj.im_class)


def _get_sync_patched(fn):
    @functools.wraps(fn)
    def _patched(*args, **kwargs):
        cdef dict to_inject = kwargs.copy()
        for injection, provider in _patched.__injections__.items():
            if injection not in kwargs \
                    or _is_fastapi_default_arg_injection(injection, kwargs):
                to_inject[injection] = provider()

        result = fn(*args, **to_inject)

        for injection, provider in _patched.__closing__.items():
            if injection in kwargs \
                    and not _is_fastapi_default_arg_injection(injection, kwargs):
                continue
            if not isinstance(provider, providers.Resource):
                continue
            provider.shutdown()

        return result
    return _patched


cdef bint _is_fastapi_default_arg_injection(object injection, dict kwargs):
    """Check if injection is FastAPI injection of the default argument."""
    return injection in kwargs and _is_marker(kwargs[injection])


cdef bint _is_marker(object instance):
    return getattr(instance, "__IS_MARKER__", False) is True
