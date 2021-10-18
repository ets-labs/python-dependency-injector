"""Provider tests."""

import warnings

from dependency_injector import providers, errors
from pytest import fixture, raises


@fixture
def provider():
    return providers.Provider()


def test_is_provider(provider):
    assert providers.is_provider(provider) is True


def test_call(provider):
    with raises(NotImplementedError):
        provider()


def test_delegate(provider):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        delegate1 = provider.delegate()
        delegate2 = provider.delegate()

    assert isinstance(delegate1, providers.Delegate)
    assert delegate1() is provider

    assert isinstance(delegate2, providers.Delegate)
    assert delegate2() is provider

    assert delegate1 is not delegate2


def test_provider(provider):
    delegate1 = provider.provider

    assert isinstance(delegate1, providers.Delegate)
    assert delegate1() is provider

    delegate2 = provider.provider

    assert isinstance(delegate2, providers.Delegate)
    assert delegate2() is provider

    assert delegate1 is not delegate2


def test_override(provider):
    overriding_provider = providers.Provider()
    provider.override(overriding_provider)
    assert provider.overridden == (overriding_provider,)
    assert provider.last_overriding is overriding_provider


def test_double_override(provider):
    overriding_provider1 = providers.Object(1)
    overriding_provider2 = providers.Object(2)

    provider.override(overriding_provider1)
    overriding_provider1.override(overriding_provider2)

    assert provider() == overriding_provider2()


def test_overriding_context(provider):
    overriding_provider = providers.Provider()
    with provider.override(overriding_provider):
        assert provider.overridden == (overriding_provider,)
    assert provider.overridden == tuple()
    assert not provider.overridden


def test_override_with_itself(provider):
    with raises(errors.Error):
        provider.override(provider)


def test_override_with_not_provider(provider):
    obj = object()
    provider.override(obj)
    assert provider() is obj


def test_reset_last_overriding(provider):
    overriding_provider1 = providers.Provider()
    overriding_provider2 = providers.Provider()

    provider.override(overriding_provider1)
    provider.override(overriding_provider2)

    assert provider.overridden[-1] is overriding_provider2
    assert provider.last_overriding is overriding_provider2

    provider.reset_last_overriding()
    assert provider.overridden[-1] is overriding_provider1
    assert provider.last_overriding is overriding_provider1

    provider.reset_last_overriding()
    assert provider.overridden == tuple()
    assert not provider.overridden
    assert provider.last_overriding is None


def test_reset_last_overriding_of_not_overridden_provider(provider):
    with raises(errors.Error):
        provider.reset_last_overriding()


def test_reset_override(provider):
    overriding_provider = providers.Provider()
    provider.override(overriding_provider)

    assert provider.overridden
    assert provider.overridden == (overriding_provider,)

    provider.reset_override()

    assert provider.overridden == tuple()


def test_deepcopy(provider):
    provider_copy = providers.deepcopy(provider)

    assert provider is not provider_copy
    assert isinstance(provider, providers.Provider)


def test_deepcopy_from_memo(provider):
    provider_copy_memo = providers.Provider()
    provider_copy = providers.deepcopy(provider, memo={id(provider): provider_copy_memo})
    assert provider_copy is provider_copy_memo


def test_deepcopy_overridden(provider):
    overriding_provider = providers.Provider()

    provider.override(overriding_provider)

    provider_copy = providers.deepcopy(provider)
    overriding_provider_copy = provider_copy.overridden[0]

    assert provider is not provider_copy
    assert isinstance(provider, providers.Provider)

    assert overriding_provider is not overriding_provider_copy
    assert isinstance(overriding_provider_copy, providers.Provider)


def test_repr(provider):
    assert repr(provider) == (
        "<dependency_injector.providers."
        "Provider() at {0}>".format(hex(id(provider)))
    )
