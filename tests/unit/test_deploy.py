import sys
from typing import AsyncIterator, Iterator

from fastapi import FastAPI
from pytest import mark, raises

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.deploy import ContainerDeploy
from dependency_injector.providers import Object, Resource
from dependency_injector.wiring import Provide, inject


@inject
def wired_value(value: str = Provide["deploy_value"]) -> object:
    return value


class ModuleDeploy(ContainerDeploy):
    @property
    def wire_modules(self):
        return [sys.modules[__name__]]


@mark.parametrize("sync", [False, True])
async def test_wires_and_initializes_resources(sync: bool) -> None:
    events = []

    def sync_resource() -> Iterator[None]:
        events.append("init")
        yield
        events.append("shutdown")

    async def async_resource() -> AsyncIterator[None]:
        events.append("init")
        yield
        events.append("shutdown")

    class Container(DeclarativeContainer):
        deploy_value = Object("wired")
        resource = Resource(sync_resource if sync else async_resource)

    async with ModuleDeploy(Container()):
        assert wired_value() == "wired"
        assert events == ["init"]

    assert wired_value() != "wired"
    assert events == ["init", "shutdown"]


async def test_discovers_modules_with_inject_callables() -> None:
    class Container(DeclarativeContainer):
        deploy_value = Object("wired")

    deploy = ContainerDeploy(Container())

    assert deploy.wire_modules == [sys.modules[__name__]]

    async with deploy:
        assert wired_value() == "wired"

    assert wired_value() != "wired"


async def test_wires_overridden_modules() -> None:
    class Container(DeclarativeContainer):
        deploy_value = Object("wired")

    async with ModuleDeploy(Container()):
        assert wired_value() == "wired"

    assert wired_value() != "wired"


async def test_wires_class_attribute_modules() -> None:
    class AttributeDeploy(ContainerDeploy):
        modules = [sys.modules[__name__]]

    class Container(DeclarativeContainer):
        deploy_value = Object("wired")

    async with AttributeDeploy(Container()):
        assert wired_value() == "wired"

    assert wired_value() != "wired"


async def test_modules_parameter_overrides_class_attribute() -> None:
    class AttributeDeploy(ContainerDeploy):
        modules = ["nonexistent.module"]

    class Container(DeclarativeContainer):
        deploy_value = Object("wired")

    deploy = AttributeDeploy(Container(), modules=[sys.modules[__name__]])

    assert deploy.wire_modules == [sys.modules[__name__]]
    assert AttributeDeploy.modules == ["nonexistent.module"]

    async with deploy:
        assert wired_value() == "wired"

    assert wired_value() != "wired"


async def test_unwires_when_init_fails() -> None:
    async def failing_resource() -> AsyncIterator[None]:
        raise RuntimeError("init failed")
        yield

    class Container(DeclarativeContainer):
        deploy_value = Object("wired")
        failing = Resource(failing_resource)

    with raises(RuntimeError, match="init failed"):
        async with ModuleDeploy(Container()):
            pass

    assert wired_value() != "wired"


async def test_unwires_when_shutdown_fails() -> None:
    async def failing_resource() -> AsyncIterator[None]:
        yield
        raise RuntimeError("shutdown failed")

    class Container(DeclarativeContainer):
        deploy_value = Object("wired")
        failing = Resource(failing_resource)

    with raises(RuntimeError, match="shutdown failed"):
        async with ModuleDeploy(Container()):
            assert wired_value() == "wired"

    assert wired_value() != "wired"


async def test_lifespan() -> None:
    class Container(DeclarativeContainer):
        deploy_value = Object("wired")

    app = FastAPI(lifespan=ModuleDeploy(Container()))

    async with app.router.lifespan_context(app):
        assert wired_value() == "wired"

    assert wired_value() != "wired"
