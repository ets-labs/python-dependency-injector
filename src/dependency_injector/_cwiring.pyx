"""Wiring optimizations module."""

import asyncio
import collections.abc
import functools
import inspect
import types

from . import providers
from .wiring import _Marker


def _get_sync_patched(fn):
    @functools.wraps(fn)
    def _patched(*args, **kwargs):
        cdef object result
        cdef dict to_inject

        to_inject = kwargs.copy()
        for injection, provider in _patched.__injections__.items():
            if injection not in kwargs or isinstance(kwargs[injection], _Marker):
                to_inject[injection] = provider()

        result = fn(*args, **to_inject)

        if _patched.__closing__:
            for injection, provider in _patched.__closing__.items():
                if injection in kwargs and not isinstance(kwargs[injection], _Marker):
                    continue
                if not isinstance(provider, providers.Resource):
                    continue
                provider.shutdown()

        return result
    return _patched


def _get_async_patched(fn):
    @functools.wraps(fn)
    async def _patched(*args, **kwargs):
        cdef object result
        cdef dict to_inject
        cdef list to_inject_await = []
        cdef list to_close_await = []

        to_inject = kwargs.copy()
        for injection, provider in _patched.__injections__.items():
            if injection not in kwargs or isinstance(kwargs[injection], _Marker):
                provide = provider()
                if _isawaitable(provide):
                    to_inject_await.append((injection, provide))
                else:
                    to_inject[injection] = provide

        if to_inject_await:
            async_to_inject = await asyncio.gather(*(provide for _, provide in to_inject_await))
            for provide, (injection, _) in zip(async_to_inject, to_inject_await):
                to_inject[injection] = provide

        result = await fn(*args, **to_inject)

        if _patched.__closing__:
            for injection, provider in _patched.__closing__.items():
                if injection in kwargs \
                        and isinstance(kwargs[injection], _Marker):
                    continue
                if not isinstance(provider, providers.Resource):
                    continue
                shutdown = provider.shutdown()
                if _isawaitable(shutdown):
                    to_close_await.append(shutdown)

            await asyncio.gather(*to_close_await)

        return result

    # Hotfix for iscoroutinefunction() for Cython < 3.0.0; can be removed after migration to Cython 3.0.0+
    _patched._is_coroutine = asyncio.coroutines._is_coroutine

    return _patched


cdef bint _isawaitable(object instance):
    """Return true if object can be passed to an ``await`` expression."""
    return (isinstance(instance, types.CoroutineType) or
            isinstance(instance, types.GeneratorType) and
            bool(instance.gi_code.co_flags & inspect.CO_ITERABLE_COROUTINE) or
            isinstance(instance, collections.abc.Awaitable))
