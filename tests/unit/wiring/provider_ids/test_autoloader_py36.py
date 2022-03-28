"""Autoloader tests."""

import contextlib
import importlib

from dependency_injector.wiring import register_loader_containers, unregister_loader_containers
from pytest import fixture

from samples.wiring import module
from samples.wiring.service import Service
from samples.wiring.container import Container


@fixture
def container():
    container = Container()

    yield container

    with contextlib.suppress(ValueError):
        unregister_loader_containers(container)
    container.unwire()
    importlib.reload(module)


def test_register_container(container: Container) -> None:
    register_loader_containers(container)
    importlib.reload(module)

    service = module.test_function()
    assert isinstance(service, Service)


def test_numpy_scipy_and_builtins_dont_break_wiring(container: Container) -> None:
    register_loader_containers(container)
    importlib.reload(module)
    importlib.import_module("samples.wiring.imports")

    service = module.test_function()

    assert isinstance(service, Service)
