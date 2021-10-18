"""Tests for wiring to module as package."""

from pytest import fixture

from samples.wiring import module
from samples.wiring.service import Service
from samples.wiring.container import Container


@fixture
def container():
    container = Container()
    yield container
    container.unwire()


def test_module_as_package_wiring(container: Container):
    # See: https://github.com/ets-labs/python-dependency-injector/issues/481
    container.wire(packages=[module])
    assert isinstance(module.service, Service)
