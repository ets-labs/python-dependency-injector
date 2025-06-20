"""Wiring optimizations module."""

from asyncio import gather
from collections.abc import Awaitable
from inspect import CO_ITERABLE_COROUTINE
from types import CoroutineType, GeneratorType

from .providers cimport Provider, Resource
from .wiring import _Marker


cdef inline bint _is_injectable(dict kwargs, object name):
    return name not in kwargs or isinstance(kwargs[name], _Marker)


cdef class DependencyResolver:
    cdef dict kwargs
    cdef dict to_inject
    cdef dict injections
    cdef dict closings

    def __init__(self, dict kwargs, dict injections, dict closings, /):
        self.kwargs = kwargs
        self.to_inject = kwargs.copy()
        self.injections = injections
        self.closings = closings

    async def _await_injection(self, name: str, value: object, /) -> None:
        self.to_inject[name] = await value

    cdef void _handle_injections_sync(self):
        cdef Provider provider

        for name, provider in self.injections.items():
            if _is_injectable(self.kwargs, name):
                self.to_inject[name] = provider()

    cdef list _handle_injections_async(self):
        cdef list to_await = []
        cdef Provider provider

        for name, provider in self.injections.items():
            if _is_injectable(self.kwargs, name):
                provide = provider()

                if provider.is_async_mode_enabled() or _isawaitable(provide):
                    to_await.append(self._await_injection(name, provide))
                else:
                    self.to_inject[name] = provide

        return to_await

    cdef void _handle_closings_sync(self):
        cdef Provider provider

        for name, provider in self.closings.items():
            if _is_injectable(self.kwargs, name) and isinstance(provider, Resource):
                provider.shutdown()

    cdef list _handle_closings_async(self):
        cdef list to_await = []
        cdef Provider provider

        for name, provider in self.closings.items():
            if _is_injectable(self.kwargs, name) and isinstance(provider, Resource):
                if _isawaitable(shutdown := provider.shutdown()):
                    to_await.append(shutdown)

        return to_await

    def __enter__(self):
        self._handle_injections_sync()
        return self.to_inject

    def __exit__(self, *_):
        self._handle_closings_sync()

    async def __aenter__(self):
        if to_await := self._handle_injections_async():
            await gather(*to_await)
        return self.to_inject

    async def __aexit__(self, *_):
        if to_await := self._handle_closings_async():
            await gather(*to_await)


cdef bint _isawaitable(object instance):
    """Return true if object can be passed to an ``await`` expression."""
    return (isinstance(instance, CoroutineType) or
            isinstance(instance, GeneratorType) and
            bool(instance.gi_code.co_flags & CO_ITERABLE_COROUTINE) or
            isinstance(instance, Awaitable))
