"""Tests for specifying wiring config in the container."""

from dependency_injector import containers
from dependency_injector.wiring import Provide
from pytest import fixture, mark

from samples.wiring import module
from samples.wiring.service import Service
from samples.wiring.container import Container


@fixture(autouse=True)
def container(wiring_config: containers.WiringConfiguration):
    original_wiring_config = Container.wiring_config
    Container.wiring_config = wiring_config
    container = Container()
    yield container
    container.unwire()
    Container.wiring_config = original_wiring_config


@mark.parametrize(
    "wiring_config",
    [
        containers.WiringConfiguration(
            modules=["samples.wiring.module"],
            packages=["samples.wiring.package"],
        ),
    ],
)
def test_absolute_names():
    service = module.test_function()
    assert isinstance(service, Service)

    from samples.wiring.package.subpackage.submodule import test_function
    service = test_function()
    assert isinstance(service, Service)


@mark.parametrize(
    "wiring_config",
    [
        containers.WiringConfiguration(
            modules=[".module"],
            packages=[".package"],
            from_package="samples.wiring",
        ),
    ],
)
def test_relative_names_with_explicit_package():
    service = module.test_function()
    assert isinstance(service, Service)

    from samples.wiring.package.subpackage.submodule import test_function
    service = test_function()
    assert isinstance(service, Service)


@mark.parametrize(
    "wiring_config",
    [
        containers.WiringConfiguration(
            modules=[".module"],
            packages=[".package"],
        ),
    ],
)
def test_relative_names_with_auto_package():
    service = module.test_function()
    assert isinstance(service, Service)

    from samples.wiring.package.subpackage.submodule import test_function
    service = test_function()
    assert isinstance(service, Service)


@mark.parametrize(
    "wiring_config",
    [
        containers.WiringConfiguration(
            modules=[".module"],
            auto_wire=False,
        ),
    ],
)
def test_auto_wire_disabled(container: Container):
    service = module.test_function()
    assert isinstance(service, Provide)

    container.wire()
    service = module.test_function()
    assert isinstance(service, Service)
