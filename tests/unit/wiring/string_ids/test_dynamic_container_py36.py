"""Tests for wiring with dynamic container."""

from dependency_injector import containers, providers
from pytest import fixture

from samples.wiringstringids import module, package
from samples.wiringstringids.service import Service


@fixture(autouse=True)
def container():
    sub = containers.DynamicContainer()
    sub.int_object = providers.Object(1)

    container = containers.DynamicContainer()
    container.config = providers.Configuration()
    container.service = providers.Factory(Service)
    container.sub = sub

    container.wire(
        modules=[module],
        packages=[package],
    )

    yield container

    container.unwire()


def test_wire():
    service = module.test_function()
    assert isinstance(service, Service)
