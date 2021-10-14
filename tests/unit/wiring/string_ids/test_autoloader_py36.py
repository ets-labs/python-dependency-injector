"""Auto loader tests."""

import contextlib
import importlib

from dependency_injector.wiring import register_loader_containers, unregister_loader_containers
from pytest import fixture

from samples.wiringstringids import module
from samples.wiringstringids.service import Service
from samples.wiringstringids.container import Container


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
