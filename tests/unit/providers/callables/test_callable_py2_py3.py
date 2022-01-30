"""Callable provider tests."""

import decimal
import sys

from dependency_injector import providers, errors
from pytest import raises, mark

from .common import example


def test_is_provider():
    assert providers.is_provider(providers.Callable(example)) is True


def test_init_with_not_callable():
    with raises(errors.Error):
        providers.Callable(123)


def test_init_optional_provides():
    provider = providers.Callable()
    provider.set_provides(object)
    assert provider.provides is object
    assert isinstance(provider(), object)


def test_set_provides_returns_():
    provider = providers.Callable()
    assert provider.set_provides(object) is provider


@mark.parametrize(
    "str_name,cls",
    [
        ("dependency_injector.providers.Factory", providers.Factory),
        ("decimal.Decimal", decimal.Decimal),
        ("list", list),
        (".common.example", example),
        ("test_is_provider", test_is_provider),
    ],
)
def test_set_provides_string_imports(str_name, cls):
    assert providers.Callable(str_name).provides is cls


def test_provided_instance_provider():
    provider = providers.Callable(example)
    assert isinstance(provider.provided, providers.ProvidedInstance)


def test_call():
    provider = providers.Callable(lambda: True)
    assert provider() is True


def test_call_with_positional_args():
    provider = providers.Callable(example, 1, 2, 3, 4)
    assert provider() == (1, 2, 3, 4)


def test_call_with_keyword_args():
    provider = providers.Callable(example, arg1=1, arg2=2, arg3=3, arg4=4)
    assert provider() == (1, 2, 3, 4)


def test_call_with_positional_and_keyword_args():
    provider = providers.Callable(example, 1, 2, arg3=3, arg4=4)
    assert provider() == (1, 2, 3, 4)


def test_call_with_context_args():
    provider = providers.Callable(example, 1, 2)
    assert provider(3, 4) == (1, 2, 3, 4)


def test_call_with_context_kwargs():
    provider = providers.Callable(example, arg1=1)
    assert provider(arg2=2, arg3=3, arg4=4) == (1, 2, 3, 4)


def test_call_with_context_args_and_kwargs():
    provider = providers.Callable(example, 1)
    assert provider(2, arg3=3, arg4=4) == (1, 2, 3, 4)


def test_fluent_interface():
    provider = providers.Singleton(example) \
        .add_args(1, 2) \
        .add_kwargs(arg3=3, arg4=4)
    assert provider() == (1, 2, 3, 4)


def test_set_args():
    provider = providers.Callable(example) \
        .add_args(1, 2) \
        .set_args(3, 4)
    assert provider.args == (3, 4)


def test_set_kwargs():
    provider = providers.Callable(example) \
        .add_kwargs(init_arg3=3, init_arg4=4) \
        .set_kwargs(init_arg3=4, init_arg4=5)
    assert provider.kwargs == dict(init_arg3=4, init_arg4=5)


def test_clear_args():
    provider = providers.Callable(example) \
        .add_args(1, 2) \
        .clear_args()
    assert provider.args == tuple()


def test_clear_kwargs():
    provider = providers.Callable(example) \
        .add_kwargs(init_arg3=3, init_arg4=4) \
        .clear_kwargs()
    assert provider.kwargs == dict()


def test_call_overridden():
    provider = providers.Callable(example)

    provider.override(providers.Object((4, 3, 2, 1)))
    provider.override(providers.Object((1, 2, 3, 4)))

    assert provider() == (1, 2, 3, 4)


def test_deepcopy():
    provider = providers.Callable(example)

    provider_copy = providers.deepcopy(provider)

    assert provider is not provider_copy
    assert provider.provides is provider_copy.provides
    assert isinstance(provider, providers.Callable)


def test_deepcopy_from_memo():
    provider = providers.Callable(example)
    provider_copy_memo = providers.Callable(example)

    provider_copy = providers.deepcopy(provider, memo={id(provider): provider_copy_memo})

    assert provider_copy is provider_copy_memo


def test_deepcopy_args():
    provider = providers.Callable(example)
    dependent_provider1 = providers.Callable(list)
    dependent_provider2 = providers.Callable(dict)

    provider.add_args(dependent_provider1, dependent_provider2)

    provider_copy = providers.deepcopy(provider)
    dependent_provider_copy1 = provider_copy.args[0]
    dependent_provider_copy2 = provider_copy.args[1]

    assert provider.args != provider_copy.args

    assert dependent_provider1.provides is dependent_provider_copy1.provides
    assert dependent_provider1 is not dependent_provider_copy1

    assert dependent_provider2.provides is dependent_provider_copy2.provides
    assert dependent_provider2 is not dependent_provider_copy2


def test_deepcopy_kwargs():
    provider = providers.Callable(example)
    dependent_provider1 = providers.Callable(list)
    dependent_provider2 = providers.Callable(dict)

    provider.add_kwargs(a1=dependent_provider1, a2=dependent_provider2)

    provider_copy = providers.deepcopy(provider)
    dependent_provider_copy1 = provider_copy.kwargs["a1"]
    dependent_provider_copy2 = provider_copy.kwargs["a2"]

    assert provider.kwargs != provider_copy.kwargs

    assert dependent_provider1.provides is dependent_provider_copy1.provides
    assert dependent_provider1 is not dependent_provider_copy1

    assert dependent_provider2.provides is dependent_provider_copy2.provides
    assert dependent_provider2 is not dependent_provider_copy2


def test_deepcopy_overridden():
    provider = providers.Callable(example)
    object_provider = providers.Object(object())

    provider.override(object_provider)

    provider_copy = providers.deepcopy(provider)
    object_provider_copy = provider_copy.overridden[0]

    assert provider is not provider_copy
    assert provider.provides is provider_copy.provides
    assert isinstance(provider, providers.Callable)

    assert object_provider is not object_provider_copy
    assert isinstance(object_provider_copy, providers.Object)


def test_deepcopy_with_sys_streams():
    provider = providers.Callable(example)
    provider.add_args(sys.stdin)
    provider.add_kwargs(a2=sys.stdout)

    provider_copy = providers.deepcopy(provider)

    assert provider is not provider_copy
    assert isinstance(provider_copy, providers.Callable)
    assert provider.args[0] is sys.stdin
    assert provider.kwargs["a2"] is sys.stdout


def test_repr():
    provider = providers.Callable(example)
    assert repr(provider) == (
        "<dependency_injector.providers."
        "Callable({0}) at {1}>".format(repr(example), hex(id(provider)))
    )
