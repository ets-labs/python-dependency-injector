"""Tests for string module and package names."""

from pytest import fixture

from wiringsamples import module
from wiringsamples.service import Service
from wiringsamples.container import Container
from wiringsamples.wire_relative_string_names import wire_with_relative_string_names


@fixture
def container():
    container = Container()
    yield container
    container.unwire()


def test_absolute_names(container: Container):
    container.wire(
        modules=["wiringsamples.module"],
        packages=["wiringsamples.package"],
    )

    service = module.test_function()
    assert isinstance(service, Service)

    from wiringsamples.package.subpackage.submodule import test_function
    service = test_function()
    assert isinstance(service, Service)


def test_relative_names_with_explicit_package(container: Container):
    container.wire(
        modules=[".module"],
        packages=[".package"],
        from_package="wiringsamples",
    )

    service = module.test_function()
    assert isinstance(service, Service)

    from wiringsamples.package.subpackage.submodule import test_function
    service = test_function()
    assert isinstance(service, Service)


def test_relative_names_with_auto_package(container: Container):
    wire_with_relative_string_names(container)

    service = module.test_function()
    assert isinstance(service, Service)

    from wiringsamples.package.subpackage.submodule import test_function
    service = test_function()
    assert isinstance(service, Service)


