"""List provider tests."""

import sys

from dependency_injector import providers


def test_is_provider():
    assert providers.is_provider(providers.List()) is True
    

def test_provided_instance_provider():
    provider = providers.List()
    assert isinstance(provider.provided, providers.ProvidedInstance)


def test_call_with_init_positional_args():
    provider = providers.List("i1", "i2")

    list1 = provider()
    list2 = provider()

    assert list1 == ["i1", "i2"]
    assert list2 == ["i1", "i2"]
    assert list1 is not list2


def test_call_with_context_args():
    provider = providers.List("i1", "i2")
    assert provider("i3", "i4") == ["i1", "i2", "i3", "i4"]


def test_fluent_interface():
    provider = providers.List() \
        .add_args(1, 2)
    assert provider() == [1, 2]


def test_set_args():
    provider = providers.List() \
        .add_args(1, 2) \
        .set_args(3, 4)
    assert provider.args == (3, 4)


def test_clear_args():
    provider = providers.List() \
        .add_args(1, 2) \
        .clear_args()
    assert provider.args == tuple()


def test_call_overridden():
    provider = providers.List(1, 2)
    overriding_provider1 = providers.List(2, 3)
    overriding_provider2 = providers.List(3, 4)

    provider.override(overriding_provider1)
    provider.override(overriding_provider2)

    instance1 = provider()
    instance2 = provider()

    assert instance1 is not instance2
    assert instance1 == [3, 4]
    assert instance2 == [3, 4]


def test_deepcopy():
    provider = providers.List(1, 2)

    provider_copy = providers.deepcopy(provider)

    assert provider is not provider_copy
    assert provider.args == provider_copy.args
    assert isinstance(provider, providers.List)


def test_deepcopy_from_memo():
    provider = providers.List(1, 2)
    provider_copy_memo = providers.List(1, 2)

    provider_copy = providers.deepcopy(provider, memo={id(provider): provider_copy_memo})
    assert provider_copy is provider_copy_memo


def test_deepcopy_args():
    provider = providers.List()
    dependent_provider1 = providers.Factory(list)
    dependent_provider2 = providers.Factory(dict)

    provider.add_args(dependent_provider1, dependent_provider2)

    provider_copy = providers.deepcopy(provider)
    dependent_provider_copy1 = provider_copy.args[0]
    dependent_provider_copy2 = provider_copy.args[1]

    assert provider.args != provider_copy.args

    assert dependent_provider1.cls is dependent_provider_copy1.cls
    assert dependent_provider1 is not dependent_provider_copy1

    assert dependent_provider2.cls is dependent_provider_copy2.cls
    assert dependent_provider2 is not dependent_provider_copy2


def test_deepcopy_overridden():
    provider = providers.List()
    object_provider = providers.Object(object())

    provider.override(object_provider)

    provider_copy = providers.deepcopy(provider)
    object_provider_copy = provider_copy.overridden[0]

    assert provider is not provider_copy
    assert provider.args == provider_copy.args
    assert isinstance(provider, providers.List)

    assert object_provider is not object_provider_copy
    assert isinstance(object_provider_copy, providers.Object)


def test_deepcopy_with_sys_streams():
    provider = providers.List()
    provider.add_args(sys.stdin, sys.stdout, sys.stderr)

    provider_copy = providers.deepcopy(provider)

    assert provider is not provider_copy
    assert isinstance(provider_copy, providers.List)
    assert provider.args[0] is sys.stdin
    assert provider.args[1] is sys.stdout
    assert provider.args[2] is sys.stderr


def test_repr():
    provider = providers.List(1, 2)
    assert repr(provider) == (
        "<dependency_injector.providers."
        "List({0}) at {1}>".format(repr(list(provider.args)), hex(id(provider)))
    )
