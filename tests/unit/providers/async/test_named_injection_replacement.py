"""Named injection replacement must discard previously registered providers."""

import inspect
from types import SimpleNamespace

from dependency_injector import providers
from pytest import mark


@mark.asyncio
@mark.parametrize("provider_type", [providers.Callable, providers.Factory, providers.Singleton,
                                    providers.Resource, providers.Dict])
@mark.parametrize("asynchronous", [False, True])
@mark.parametrize("context", [{}, {"extra": 42}])
async def test_add_kwargs_replaces_existing_injection(provider_type, asynchronous, context):
    calls = []

    def original():
        calls.append(True)
        return "original"

    async def original_async():
        return original()

    dependency = providers.Callable(original_async if asynchronous else original)
    if provider_type is providers.Dict:
        provider = provider_type(value=dependency)
    else:
        provider = provider_type(dict, value=dependency)
    provider.add_kwargs(value="intermediate").add_kwargs(value="replacement")

    result = provider(**context)
    if inspect.isawaitable(result):
        result = await result

    assert result == dict(value="replacement", **context)
    assert calls == []
    assert provider.kwargs == {"value": "replacement"}


@mark.asyncio
@mark.parametrize("provider_type", [providers.Factory, providers.Singleton])
async def test_add_attributes_replaces_async_injection(provider_type):
    calls = []

    async def original():
        calls.append(True)
        return "original"

    provider = provider_type(SimpleNamespace)
    provider.add_attributes(value=providers.Callable(original))
    provider.add_attributes(value="replacement")
    result = provider()
    if inspect.isawaitable(result):
        result = await result

    assert result.value == "replacement"
    assert calls == []


@mark.asyncio
@mark.parametrize("method", ["__init__", "add_kwargs", "set_kwargs"])
async def test_dict_keyword_overrides_mapping_injection(method):
    calls = []

    async def original():
        calls.append(True)
        return "original"

    provider = providers.Dict()
    getattr(provider, method)({"value": providers.Callable(original)}, value="replacement")
    result = provider()
    if inspect.isawaitable(result):
        result = await result

    assert result == {"value": "replacement"}
    assert calls == []


@mark.asyncio
@mark.parametrize("provider_type", [providers.Callable, providers.Factory, providers.Singleton,
                                    providers.Resource, providers.Dict])
@mark.parametrize("override", [False, True])
async def test_async_replacement_and_call_time_precedence(provider_type, override):
    calls = []

    async def replacement():
        calls.append(True)
        return "replacement"

    if provider_type is providers.Dict:
        provider = provider_type(value="original")
    else:
        provider = provider_type(dict, value="original")
    provider.add_kwargs(value=providers.Callable(replacement))
    result = provider(**({"value": "explicit"} if override else {}))
    if inspect.isawaitable(result):
        result = await result

    assert result == {"value": "explicit" if override else "replacement"}
    assert calls == ([] if override else [True])
