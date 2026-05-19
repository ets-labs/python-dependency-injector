"""Wiring discovery against Cython-compiled user modules."""

import pytest

pytest.importorskip("Cython")

import pyximport  # noqa: E402

pyximport.install(language_level=3)

cythonmodule = pytest.importorskip(
    "samples.wiringcython.cythonmodule",
    reason="Cython fixture not built (Cython / C toolchain missing)",
)

from samples.wiringcython.container import Container, Service  # noqa: E402

from dependency_injector import providers  # noqa: E402
from dependency_injector.wiring import (  # noqa: E402
    _is_cyfunction,
    _is_function_like,
    _patched_registry,
)


@pytest.fixture
def container():
    c = Container()
    c.wire(modules=[cythonmodule])
    yield c
    c.unwire()


def _pure_python_fn():
    pass


@pytest.mark.parametrize(
    "obj,is_cy,is_func_like",
    [
        pytest.param(lambda: cythonmodule.sync_handler, True, True, id="cython-sync"),
        pytest.param(lambda: cythonmodule.async_handler, True, True, id="cython-async"),
        pytest.param(
            lambda: cythonmodule.async_gen_handler, True, True, id="cython-async-gen"
        ),
        pytest.param(
            lambda: cythonmodule.HandlerClass.__call__,
            True,
            True,
            id="cython-class-call",
        ),
        pytest.param(lambda: _pure_python_fn, False, True, id="pure-python"),
    ],
)
def test_function_like_predicate(obj, is_cy, is_func_like):
    target = obj()
    assert _is_cyfunction(target) is is_cy
    assert _is_function_like(target) is is_func_like


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


def test_sync_handler_respects_provider_override(container):
    with container.service.override(providers.Object(Service(value="overridden"))):
        assert cythonmodule.sync_handler() == "overridden"
    assert cythonmodule.sync_handler() == "injected"


def test_unwire_clears_injection_bindings_on_compiled_module():
    c = Container()
    c.wire(modules=[cythonmodule])

    wrapper = cythonmodule.sync_handler
    patched = _patched_registry.get_callable(wrapper)

    assert patched is not None
    assert patched.reference_injections
    assert patched.injections

    c.unwire()

    assert patched.injections == {}
    assert patched.reference_injections
