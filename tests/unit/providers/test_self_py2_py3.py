"""Self provider tests."""

from dependency_injector import providers, containers


def test_is_provider():
    assert providers.is_provider(providers.Self()) is True


def test_call_object_provider():
    container = containers.DeclarativeContainer()
    assert providers.Self(container)() is container


def test_set_container():
    container = containers.DeclarativeContainer()
    provider = providers.Self()
    provider.set_container(container)
    assert provider() is container


def test_set_alt_names():
    provider = providers.Self()
    provider.set_alt_names({"foo", "bar", "baz"})
    assert set(provider.alt_names) == {"foo", "bar", "baz"}


def test_deepcopy():
    provider = providers.Self()

    provider_copy = providers.deepcopy(provider)

    assert provider is not provider_copy
    assert isinstance(provider, providers.Self)


def test_deepcopy_from_memo():
    provider = providers.Self()
    provider_copy_memo = providers.Provider()

    provider_copy = providers.deepcopy(provider, memo={id(provider): provider_copy_memo})

    assert provider_copy is provider_copy_memo


def test_deepcopy_overridden():
    provider = providers.Self()
    overriding_provider = providers.Provider()

    provider.override(overriding_provider)

    provider_copy = providers.deepcopy(provider)
    overriding_provider_copy = provider_copy.overridden[0]

    assert provider is not provider_copy
    assert isinstance(provider, providers.Self)

    assert overriding_provider is not overriding_provider_copy
    assert isinstance(overriding_provider_copy, providers.Provider)


def test_repr():
    container = containers.DeclarativeContainer()
    provider = providers.Self(container)
    assert repr(provider) == (
        "<dependency_injector.providers."
        "Self({0}) at {1}>".format(repr(container), hex(id(provider)))
    )
