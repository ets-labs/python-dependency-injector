# cython: language_level=3, binding=True, embedsignature=True, annotation_typing=False
"""Cython-compiled fixture exercising wire() against compiled handlers.

Compiled by tests/unit/wiring/conftest.py::pytest_configure with the four
directives FastAPI / dependency-injector codebases require:

  binding=True              — preserve descriptor semantics (so inspect.signature
                              + DI introspection work)
  embedsignature=True       — embed Python-style signature for inspect.signature
  annotation_typing=False   — annotations stay informational; do NOT generate
                              C-level isinstance checks against parameter defaults
                              (the FastAPI `param: str = Header(...)` pattern
                              relies on this)
  language_level=3          — pure Python 3 semantics

Exercises every call shape the wiring discovery pass dispatches on:

  - sync def at module level                    -> _get_sync_patched
  - async def at module level                   -> _get_async_patched
  - async def with yield (async generator)      -> _get_async_gen_patched
  - class with async def __call__               -> _patch_method
"""

from dependency_injector.wiring import Provide

from samples.wiringcython.container import Container, Service


def sync_handler(svc: Service = Provide[Container.service]) -> str:
    return svc.get()


async def async_handler(svc: Service = Provide[Container.service]) -> str:
    return await svc.aget()


async def async_gen_handler(svc: Service = Provide[Container.service]):
    yield svc.get()
    yield svc.get() + "_2"


class HandlerClass:
    async def __call__(self, svc: Service = Provide[Container.service]) -> str:
        return svc.get()
