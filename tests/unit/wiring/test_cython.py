"""Regression coverage: wiring discovery against Cython-compiled user modules.

Builds the .pyx fixture in conftest.py::pytest_configure, then asserts every
callable shape the wire() dispatch handles is correctly recognised AND
runtime-injected when compiled to a .so:

  - module-level sync ``def``
  - module-level ``async def``
  - module-level async-generator ``async def`` with ``yield``
  - class with async ``def __call__``

Also asserts the cyfunction detection helpers behave correctly on both
compiled and pure-Python callables, exercises the ``CO_COROUTINE`` /
``CO_ASYNC_GENERATOR`` fallback branches via a synthetic code object,
and pins the descriptor type for class-attribute ``__call__`` so future
Cython releases that change the attribute representation surface as a
test failure rather than a silent regression.

If Cython / setuptools / a C compiler is unavailable in the test
environment, the whole module is skipped via pytest.importorskip.
"""

from inspect import CO_ASYNC_GENERATOR, CO_COROUTINE

import pytest

cythonmodule = pytest.importorskip(
    "samples.wiringcython.cythonmodule",
    reason="Cython fixture not built (Cython/setuptools/C toolchain missing)",
)

# Catch the silent-skip-on-empty-module case: ``pytest.importorskip`` falls
# through cleanly when the import succeeds even if the resulting module is
# missing the symbols this test suite depends on. Without this check, a
# regressed fixture (or a stray .so from a different revision) lets pytest
# report "0 items collected" as a successful empty pass — exactly the
# false-green CI mode that motivated the rest of this file. Fail loudly at
# collection time instead.
for _sym in ("sync_handler", "async_handler", "async_gen_handler", "HandlerClass"):
    if not hasattr(cythonmodule, _sym):
        raise AssertionError(
            f"Cython fixture is missing required symbol: {_sym}. "
            "The .so was importable but doesn't contain the expected handlers — "
            "rebuild or clean stale artefacts under "
            "tests/unit/samples/wiringcython/."
        )

from samples.wiringcython.container import Container, Service  # noqa: E402

from dependency_injector import providers  # noqa: E402
from dependency_injector.wiring import (  # noqa: E402
    _is_cyfunction,
    _is_function_like,
    _isasyncgenfunction_compat,
    _iscoroutinefunction_compat,
    _patched_registry,
)


@pytest.fixture
def container():
    c = Container()
    c.wire(modules=[cythonmodule])
    yield c
    c.unwire()


# -- discovery helpers --------------------------------------------------------


def test_is_cyfunction_recognises_compiled_handlers():
    assert _is_cyfunction(cythonmodule.sync_handler)
    assert _is_cyfunction(cythonmodule.async_handler)
    assert _is_cyfunction(cythonmodule.async_gen_handler)


def test_is_cyfunction_rejects_pure_python():
    def py_fn():
        pass

    assert not _is_cyfunction(py_fn)


def test_is_function_like_accepts_both():
    def py_fn():
        pass

    assert _is_function_like(py_fn)
    assert _is_function_like(cythonmodule.sync_handler)


def test_iscoroutinefunction_compat_on_cython_async_def():
    assert _iscoroutinefunction_compat(cythonmodule.async_handler)
    assert not _iscoroutinefunction_compat(cythonmodule.sync_handler)


def test_isasyncgenfunction_compat_on_cython_async_gen():
    assert _isasyncgenfunction_compat(cythonmodule.async_gen_handler)
    assert not _isasyncgenfunction_compat(cythonmodule.async_handler)
    assert not _isasyncgenfunction_compat(cythonmodule.sync_handler)


# -- fallback-branch coverage (H4 — synthetic code objects) ------------------
#
# Under Cython >= 3.0 the inspect.iscoroutinefunction / isasyncgenfunction
# checks already return True for compiled async / async-generator
# cyfunctions, so the ``__code__.co_flags`` fallback inside the compat
# helpers is unreachable from the fixture above. Exercise it directly
# with a callable carrying a forged ``__code__`` so the branch is covered.


class _FakeCode:
    def __init__(self, co_flags: int) -> None:
        self.co_flags = co_flags


class _FakeCallable:
    """Inspection-only stand-in for an async cyfunction built on Cython < 3.

    ``inspect.iscoroutinefunction`` and ``isasyncgenfunction`` both return
    False for instances of arbitrary classes — exactly the
    pre-Cython-3.0 cyfunction shape the fallback was written for.
    """

    def __init__(self, co_flags: int) -> None:
        self.__code__ = _FakeCode(co_flags)


def test_iscoroutinefunction_compat_falls_back_to_co_flags():
    fake_coro = _FakeCallable(CO_COROUTINE)
    fake_plain = _FakeCallable(0)
    assert _iscoroutinefunction_compat(fake_coro)
    assert not _iscoroutinefunction_compat(fake_plain)


def test_isasyncgenfunction_compat_falls_back_to_co_flags():
    fake_asyncgen = _FakeCallable(CO_ASYNC_GENERATOR)
    fake_plain = _FakeCallable(0)
    assert _isasyncgenfunction_compat(fake_asyncgen)
    assert not _isasyncgenfunction_compat(fake_plain)


def test_compat_helpers_handle_objects_without_code_attribute():
    """Lambdas / callable objects with no ``__code__`` must not crash."""

    class _NoCode:
        pass

    assert not _iscoroutinefunction_compat(_NoCode())
    assert not _isasyncgenfunction_compat(_NoCode())


# -- descriptor-type pin (M7) ------------------------------------------------


def test_handler_class_call_is_function_like():
    """Pin the descriptor representation of an ``async def __call__`` on a
    Cython-compiled class so a future Cython release that swaps it for a
    different descriptor surfaces as a failure here, not as silent
    wiring drop-out.
    """
    assert _is_function_like(cythonmodule.HandlerClass.__call__)


# -- runtime injection across all callable shapes ----------------------------


def test_sync_handler_wired(container):
    assert cythonmodule.sync_handler() == "injected"


@pytest.mark.asyncio
async def test_async_handler_wired(container):
    assert await cythonmodule.async_handler() == "injected"


@pytest.mark.asyncio
async def test_async_gen_handler_wired(container):
    results = [v async for v in cythonmodule.async_gen_handler()]
    assert results == ["injected", "injected_2"]


@pytest.mark.asyncio
async def test_class_method_wired(container):
    handler = cythonmodule.HandlerClass()
    assert await handler() == "injected"


# -- override semantics survive compile boundary -----------------------------


def test_sync_handler_respects_provider_override(container):
    with container.service.override(providers.Object(Service(value="overridden"))):
        assert cythonmodule.sync_handler() == "overridden"
    assert cythonmodule.sync_handler() == "injected"


# -- unwire empties injection bindings (C1 — positive assertion) -------------
#
# ``_unpatch`` does not restore the original attribute; it calls
# ``_unbind_injections(fn)``, which invokes
# ``PatchedCallable.unwind_injections()`` and empties the ``injections``
# dict in-place. The earlier version of this test caught any exception
# from a post-unwire call — false-pass shape, because the cyfunction
# raises ``AttributeError`` from a ``_Marker.get()`` lookup either way.
# Pin the actual contract instead: the registered ``PatchedCallable``
# has its ``injections`` dict cleared while ``reference_injections`` is
# retained (so re-wiring can re-resolve without re-running discovery).


def test_unwire_clears_injection_bindings_on_compiled_module():
    c = Container()
    c.wire(modules=[cythonmodule])

    # After wire, the module attribute is the patched wrapper. The
    # registry maps wrapper -> PatchedCallable.
    wrapper = cythonmodule.sync_handler
    patched = _patched_registry.get_callable(wrapper)

    assert patched is not None, (
        "wire() did not register the cyfunction in the patched registry"
    )
    assert patched.reference_injections, (
        "wire() did not discover any reference injections on the cyfunction"
    )
    assert patched.injections, (
        "wire() did not bind any runtime injections on the cyfunction"
    )

    c.unwire()

    assert patched.injections == {}, (
        "unwire() did not clear runtime injection bindings"
    )
    # ``reference_injections`` is preserved across unwire so a subsequent
    # wire() call can rebind without re-running discovery.
    assert patched.reference_injections, (
        "unwire() unexpectedly discarded reference_injections"
    )
