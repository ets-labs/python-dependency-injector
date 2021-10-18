"""AbstractCoroutine provider tests."""

import asyncio

from dependency_injector import providers, errors
from pytest import mark, raises

from .common import example


def test_inheritance():
    assert isinstance(providers.AbstractCoroutine(example), providers.Coroutine)


@mark.asyncio
@mark.filterwarnings("ignore")
async def test_call_overridden_by_coroutine():
    @asyncio.coroutine
    def abstract_example():
        raise RuntimeError("Should not be raised")

    provider = providers.AbstractCoroutine(abstract_example)
    provider.override(providers.Coroutine(example))

    result = await provider(1, 2, 3, 4)
    assert result == (1, 2, 3, 4)


@mark.asyncio
@mark.filterwarnings("ignore")
async def test_call_overridden_by_delegated_coroutine():
    @asyncio.coroutine
    def abstract_example():
        raise RuntimeError("Should not be raised")

    provider = providers.AbstractCoroutine(abstract_example)
    provider.override(providers.DelegatedCoroutine(example))

    result = await provider(1, 2, 3, 4)
    assert result == (1, 2, 3, 4)


def test_call_not_overridden():
    provider = providers.AbstractCoroutine(example)
    with raises(errors.Error):
        provider(1, 2, 3, 4)


def test_override_by_not_coroutine():
    provider = providers.AbstractCoroutine(example)
    with raises(errors.Error):
        provider.override(providers.Factory(object))


def test_provide_not_implemented():
    provider = providers.AbstractCoroutine(example)
    with raises(NotImplementedError):
        provider._provide((1, 2, 3, 4), dict())


def test_repr():
    provider = providers.AbstractCoroutine(example)
    assert repr(provider) == (
        "<dependency_injector.providers."
        "AbstractCoroutine({0}) at {1}>".format(repr(example), hex(id(provider)))
    )
