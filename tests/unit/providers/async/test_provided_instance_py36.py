"""ProvidedInstance provider async mode tests."""

import asyncio

from dependency_injector import containers, providers
from pytest import mark, raises

from .common import RESOURCE1, init_resource


@mark.asyncio
async def test_provided_attribute():
    class TestClient:
        def __init__(self, resource):
            self.resource = resource

    class TestService:
        def __init__(self, resource):
            self.resource = resource

    class TestContainer(containers.DeclarativeContainer):
        resource = providers.Resource(init_resource, providers.Object(RESOURCE1))
        client = providers.Factory(TestClient, resource=resource)
        service = providers.Factory(TestService, resource=client.provided.resource)

    container = TestContainer()

    instance1, instance2 = await asyncio.gather(
        container.service(),
        container.service(),
    )

    assert instance1.resource is RESOURCE1
    assert instance2.resource is RESOURCE1
    assert instance1.resource is instance2.resource


@mark.asyncio
async def test_provided_attribute_error():
    async def raise_exception():
        raise RuntimeError()

    class TestContainer(containers.DeclarativeContainer):
        client = providers.Factory(raise_exception)

    container = TestContainer()

    with raises(RuntimeError):
        await container.client.provided.attr()


@mark.asyncio
async def test_provided_attribute_undefined_attribute():
    class TestClient:
        def __init__(self, resource):
            self.resource = resource

    class TestContainer(containers.DeclarativeContainer):
        resource = providers.Resource(init_resource, providers.Object(RESOURCE1))
        client = providers.Factory(TestClient, resource=resource)

    container = TestContainer()

    with raises(AttributeError):
        await container.client.provided.attr()


@mark.asyncio
async def test_provided_item():
    class TestClient:
        def __init__(self, resource):
            self.resource = resource

        def __getitem__(self, item):
            return getattr(self, item)

    class TestService:
        def __init__(self, resource):
            self.resource = resource

    class TestContainer(containers.DeclarativeContainer):
        resource = providers.Resource(init_resource, providers.Object(RESOURCE1))
        client = providers.Factory(TestClient, resource=resource)
        service = providers.Factory(TestService, resource=client.provided["resource"])

    container = TestContainer()

    instance1, instance2 = await asyncio.gather(
        container.service(),
        container.service(),
    )

    assert instance1.resource is RESOURCE1
    assert instance2.resource is RESOURCE1
    assert instance1.resource is instance2.resource


@mark.asyncio
async def test_provided_item_error():
    async def raise_exception():
        raise RuntimeError()

    class TestContainer(containers.DeclarativeContainer):
        client = providers.Factory(raise_exception)

    container = TestContainer()

    with raises(RuntimeError):
        await container.client.provided["item"]()


@mark.asyncio
async def test_provided_item_undefined_item():
    class TestContainer(containers.DeclarativeContainer):
        resource = providers.Resource(init_resource, providers.Object(RESOURCE1))
        client = providers.Factory(dict, resource=resource)

    container = TestContainer()

    with raises(KeyError):
        await container.client.provided["item"]()


@mark.asyncio
async def test_provided_method_call():
    class TestClient:
        def __init__(self, resource):
            self.resource = resource

        def get_resource(self):
            return self.resource

    class TestService:
        def __init__(self, resource):
            self.resource = resource

    class TestContainer(containers.DeclarativeContainer):
        resource = providers.Resource(init_resource, providers.Object(RESOURCE1))
        client = providers.Factory(TestClient, resource=resource)
        service = providers.Factory(TestService, resource=client.provided.get_resource.call())

    container = TestContainer()

    instance1, instance2 = await asyncio.gather(
        container.service(),
        container.service(),
    )

    assert instance1.resource is RESOURCE1
    assert instance2.resource is RESOURCE1
    assert instance1.resource is instance2.resource


@mark.asyncio
async def test_provided_method_call_parent_error():
    async def raise_exception():
        raise RuntimeError()

    class TestContainer(containers.DeclarativeContainer):
        client = providers.Factory(raise_exception)

    container = TestContainer()

    with raises(RuntimeError):
        await container.client.provided.method.call()()


@mark.asyncio
async def test_provided_method_call_error():
    class TestClient:
        def method(self):
            raise RuntimeError()

    class TestContainer(containers.DeclarativeContainer):
        client = providers.Factory(TestClient)

    container = TestContainer()

    with raises(RuntimeError):
        await container.client.provided.method.call()()
