"""Dict provider tests."""

import sys

from dependency_injector import providers


def test_is_provider():
    assert providers.is_provider(providers.Dict()) is True


def test_provided_instance_provider():
    provider = providers.Dict()
    assert isinstance(provider.provided, providers.ProvidedInstance)


def test_init_with_non_string_keys():
    a1 = object()
    a2 = object()
    provider = providers.Dict({a1: "i1", a2: "i2"})

    dict1 = provider()
    dict2 = provider()

    assert dict1 == {a1: "i1", a2: "i2"}
    assert dict2 == {a1: "i1", a2: "i2"}

    assert dict1 is not dict2


def test_init_with_string_and_non_string_keys():
    a1 = object()
    provider = providers.Dict({a1: "i1"}, a2="i2")

    dict1 = provider()
    dict2 = provider()

    assert dict1 == {a1: "i1", "a2": "i2"}
    assert dict2 == {a1: "i1", "a2": "i2"}

    assert dict1 is not dict2


def test_call_with_init_keyword_args():
    provider = providers.Dict(a1="i1", a2="i2")

    dict1 = provider()
    dict2 = provider()

    assert dict1 == {"a1": "i1", "a2": "i2"}
    assert dict2 == {"a1": "i1", "a2": "i2"}

    assert dict1 is not dict2


def test_call_with_context_keyword_args():
    provider = providers.Dict(a1="i1", a2="i2")
    assert provider(a3="i3", a4="i4") == {"a1": "i1", "a2": "i2", "a3": "i3", "a4": "i4"}


def test_call_with_provider():
    provider = providers.Dict(
        a1=providers.Factory(str, "i1"),
        a2=providers.Factory(str, "i2"),
    )
    assert provider() == {"a1": "i1", "a2": "i2"}


def test_fluent_interface():
    provider = providers.Dict() \
        .add_kwargs(a1="i1", a2="i2")
    assert provider() == {"a1": "i1", "a2": "i2"}


def test_add_kwargs():
    provider = providers.Dict() \
        .add_kwargs(a1="i1") \
        .add_kwargs(a2="i2")
    assert provider.kwargs == {"a1": "i1", "a2": "i2"}


def test_add_kwargs_non_string_keys():
    a1 = object()
    a2 = object()
    provider = providers.Dict() \
        .add_kwargs({a1: "i1"}) \
        .add_kwargs({a2: "i2"})
    assert provider.kwargs == {a1: "i1", a2: "i2"}


def test_add_kwargs_string_and_non_string_keys():
    a2 = object()
    provider = providers.Dict() \
        .add_kwargs(a1="i1") \
        .add_kwargs({a2: "i2"})
    assert provider.kwargs == {"a1": "i1", a2: "i2"}


def test_set_kwargs():
    provider = providers.Dict() \
        .add_kwargs(a1="i1", a2="i2") \
        .set_kwargs(a3="i3", a4="i4")
    assert provider.kwargs == {"a3": "i3", "a4": "i4"}


def test_set_kwargs_non_string_keys():
    a3 = object()
    a4 = object()
    provider = providers.Dict() \
        .add_kwargs(a1="i1", a2="i2") \
        .set_kwargs({a3: "i3", a4: "i4"})
    assert provider.kwargs == {a3: "i3", a4: "i4"}


def test_set_kwargs_string_and_non_string_keys():
    a3 = object()
    provider = providers.Dict() \
        .add_kwargs(a1="i1", a2="i2") \
        .set_kwargs({a3: "i3"}, a4="i4")
    assert provider.kwargs == {a3: "i3", "a4": "i4"}


def test_clear_kwargs():
    provider = providers.Dict() \
        .add_kwargs(a1="i1", a2="i2") \
        .clear_kwargs()
    assert provider.kwargs == {}


def test_call_overridden():
    provider = providers.Dict(a1="i1", a2="i2")
    overriding_provider1 = providers.Dict(a2="i2", a3="i3")
    overriding_provider2 = providers.Dict(a3="i3", a4="i4")

    provider.override(overriding_provider1)
    provider.override(overriding_provider2)

    instance1 = provider()
    instance2 = provider()

    assert instance1 is not instance2
    assert instance1 == {"a3": "i3", "a4": "i4"}
    assert instance2 == {"a3": "i3", "a4": "i4"}


def test_deepcopy():
    provider = providers.Dict(a1="i1", a2="i2")

    provider_copy = providers.deepcopy(provider)

    assert provider is not provider_copy
    assert provider.kwargs == provider_copy.kwargs
    assert isinstance(provider, providers.Dict)


def test_deepcopy_from_memo():
    provider = providers.Dict(a1="i1", a2="i2")
    provider_copy_memo = providers.Dict(a1="i1", a2="i2")

    provider_copy = providers.deepcopy(
        provider,
        memo={id(provider): provider_copy_memo},
    )

    assert provider_copy is provider_copy_memo


def test_deepcopy_kwargs():
    provider = providers.Dict()
    dependent_provider1 = providers.Factory(list)
    dependent_provider2 = providers.Factory(dict)

    provider.add_kwargs(d1=dependent_provider1, d2=dependent_provider2)

    provider_copy = providers.deepcopy(provider)
    dependent_provider_copy1 = provider_copy.kwargs["d1"]
    dependent_provider_copy2 = provider_copy.kwargs["d2"]

    assert provider.kwargs != provider_copy.kwargs

    assert dependent_provider1.cls is dependent_provider_copy1.cls
    assert dependent_provider1 is not dependent_provider_copy1

    assert dependent_provider2.cls is dependent_provider_copy2.cls
    assert dependent_provider2 is not dependent_provider_copy2


def test_deepcopy_kwargs_non_string_keys():
    a1 = object()
    a2 = object()

    dependent_provider1 = providers.Factory(list)
    dependent_provider2 = providers.Factory(dict)

    provider = providers.Dict({a1: dependent_provider1, a2: dependent_provider2})

    provider_copy = providers.deepcopy(provider)
    dependent_provider_copy1 = provider_copy.kwargs[a1]
    dependent_provider_copy2 = provider_copy.kwargs[a2]

    assert provider.kwargs != provider_copy.kwargs

    assert dependent_provider1.cls is dependent_provider_copy1.cls
    assert dependent_provider1 is not dependent_provider_copy1

    assert dependent_provider2.cls is dependent_provider_copy2.cls
    assert dependent_provider2 is not dependent_provider_copy2


def test_deepcopy_overridden():
    provider = providers.Dict()
    object_provider = providers.Object(object())

    provider.override(object_provider)

    provider_copy = providers.deepcopy(provider)
    object_provider_copy = provider_copy.overridden[0]

    assert provider is not provider_copy
    assert provider.kwargs == provider_copy.kwargs
    assert isinstance(provider, providers.Dict)

    assert object_provider is not object_provider_copy
    assert isinstance(object_provider_copy, providers.Object)


def test_deepcopy_with_sys_streams():
    provider = providers.Dict()
    provider.add_kwargs(stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)

    provider_copy = providers.deepcopy(provider)

    assert provider is not provider_copy
    assert isinstance(provider_copy, providers.Dict)
    assert provider.kwargs["stdin"] is sys.stdin
    assert provider.kwargs["stdout"] is sys.stdout
    assert provider.kwargs["stderr"] is sys.stderr


def test_repr():
    provider = providers.Dict(a1=1, a2=2)
    assert repr(provider) == (
        "<dependency_injector.providers."
        "Dict({0}) at {1}>".format(repr(provider.kwargs), hex(id(provider)))
    )
