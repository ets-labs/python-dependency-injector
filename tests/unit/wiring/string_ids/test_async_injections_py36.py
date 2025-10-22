"""Async injection tests."""

import asyncio

from pytest import fixture, mark
from samples.wiringstringids import asyncinjections


@fixture(autouse=True)
def container():
    container = asyncinjections.Container()
    container.wire(modules=[asyncinjections])
    yield container
    container.unwire()


@fixture(autouse=True)
def reset_counters():
    asyncinjections.resource1.reset_counters()
    asyncinjections.resource2.reset_counters()


@mark.asyncio
async def test_async_injections():
    resource1, resource2 = await asyncinjections.async_injection()

    assert resource1 is asyncinjections.resource1
    assert asyncinjections.resource1.init_counter == 1
    assert asyncinjections.resource1.shutdown_counter == 0

    assert resource2 is asyncinjections.resource2
    assert asyncinjections.resource2.init_counter == 1
    assert asyncinjections.resource2.shutdown_counter == 0


@mark.asyncio
async def test_async_injections_with_closing():
    resource1, resource2, context_local_resource = await asyncinjections.async_injection_with_closing()

    assert resource1 is asyncinjections.resource1
    assert asyncinjections.resource1.init_counter == 1
    assert asyncinjections.resource1.shutdown_counter == 1

    assert resource2 is asyncinjections.resource2
    assert asyncinjections.resource2.init_counter == 1
    assert asyncinjections.resource2.shutdown_counter == 1

    assert context_local_resource is asyncinjections.resource3
    assert asyncinjections.resource3.init_counter == 1
    assert asyncinjections.resource3.shutdown_counter == 1

    resource1, resource2, context_local_resource = await asyncinjections.async_injection_with_closing()

    assert resource1 is asyncinjections.resource1
    assert asyncinjections.resource1.init_counter == 2
    assert asyncinjections.resource1.shutdown_counter == 2

    assert resource2 is asyncinjections.resource2
    assert asyncinjections.resource2.init_counter == 2
    assert asyncinjections.resource2.shutdown_counter == 2

    assert context_local_resource is asyncinjections.resource3
    assert asyncinjections.resource3.init_counter == 2
    assert asyncinjections.resource3.shutdown_counter == 2


@mark.asyncio
async def test_async_injections_with_closing_concurrently():
    resource1, resource2 = await asyncio.gather(asyncinjections.async_injection_with_closing_context_local_resources(),
                                                asyncinjections.async_injection_with_closing_context_local_resources())
    assert resource1 != resource2

    resource1 = await asyncinjections.Container.context_local_resource_with_factory_object()
    resource2 = await asyncinjections.Container.context_local_resource_with_factory_object()

    assert resource1 == resource2
