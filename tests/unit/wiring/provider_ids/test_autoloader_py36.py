"""Auto loader tests."""

import contextlib
import importlib

from pytest import fixture
from dependency_injector.wiring import register_loader_containers, unregister_loader_containers

from wiringsamples import module
from wiringsamples.service import Service
from wiringsamples.container import Container


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
    importlib.import_module("wiringsamples.imports")

    service = module.test_function()

    assert isinstance(service, Service)
