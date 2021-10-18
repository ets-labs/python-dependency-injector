"""Selector provider tests."""

import functools
import itertools
import sys

from dependency_injector import providers, errors
from pytest import fixture, mark, raises


@fixture
def switch():
    return providers.Configuration()


@fixture
def one():
    return providers.Object(1)


@fixture
def two():
    return providers.Object(2)


@fixture
def selector_type():
    return "default"


@fixture
def selector(selector_type, switch, one, two):
    if selector_type == "default":
        return providers.Selector(switch, one=one, two=two)
    elif selector_type == "empty":
        return providers.Selector()
    elif selector_type == "sys-streams":
        return providers.Selector(
            switch,
            stdin=providers.Object(sys.stdin),
            stdout=providers.Object(sys.stdout),
            stderr=providers.Object(sys.stderr),
        )
    else:
        raise ValueError("Unknown selector type \"{0}\"".format(selector_type))


def test_is_provider(selector):
    assert providers.is_provider(selector) is True


@mark.parametrize("selector_type", ["empty"])
def test_init_optional(selector, switch, one, two):
    selector.set_selector(switch)
    selector.set_providers(one=one, two=two)

    assert selector.providers == {"one": one, "two": two}
    with switch.override("one"):
        assert selector() == one()
    with switch.override("two"):
        assert selector() == two()


def test_set_selector_returns_self(selector, switch):
    assert selector.set_selector(switch) is selector


def test_set_providers_returns_self(selector, one):
    assert selector.set_providers(one=one) is selector


def test_provided_instance_provider(selector):
    assert isinstance(selector.provided, providers.ProvidedInstance)


def test_call(selector, switch):
    with switch.override("one"):
        assert selector() == 1

    with switch.override("two"):
        assert selector() == 2


def test_call_undefined_provider(selector, switch):
    with switch.override("three"):
        with raises(errors.Error):
            selector()


def test_call_selector_is_none(selector, switch):
    with switch.override(None):
        with raises(errors.Error):
            selector()


@mark.parametrize("selector_type", ["empty"])
def test_call_any_callable(selector):
    selector.set_selector(functools.partial(next, itertools.cycle(["one", "two"])))
    selector.set_providers(
        one=providers.Object(1),
        two=providers.Object(2),
    )

    assert selector() == 1
    assert selector() == 2
    assert selector() == 1
    assert selector() == 2


@mark.parametrize("selector_type", ["empty"])
def test_call_with_context_args(selector, switch):
    selector.set_selector(switch)
    selector.set_providers(one=providers.Callable(lambda *args, **kwargs: (args, kwargs)))

    with switch.override("one"):
        args, kwargs = selector(1, 2, three=3, four=4)

    assert args == (1, 2)
    assert kwargs == {"three": 3, "four": 4}


def test_getattr(selector, one, two):
    assert selector.one is one
    assert selector.two is two


def test_getattr_attribute_error(selector):
    with raises(AttributeError):
        _ = selector.provider_three


def test_call_overridden(selector, switch):
    overriding_provider1 = providers.Selector(switch, one=providers.Object(2))
    overriding_provider2 = providers.Selector(switch, one=providers.Object(3))

    selector.override(overriding_provider1)
    selector.override(overriding_provider2)

    with switch.override("one"):
        assert selector() == 3


def test_providers_attribute(selector, one, two):
    assert selector.providers == {"one": one, "two": two}


def test_deepcopy(selector):
    provider_copy = providers.deepcopy(selector)

    assert provider_copy is not selector
    assert isinstance(selector, providers.Selector)

    assert provider_copy.selector is not selector.selector
    assert isinstance(provider_copy.selector, providers.Configuration)

    assert provider_copy.one is not selector.one
    assert isinstance(provider_copy.one, providers.Object)
    assert provider_copy.one.provides == 1

    assert provider_copy.two is not selector.two
    assert isinstance(provider_copy.two, providers.Object)
    assert provider_copy.two.provides == 2


def test_deepcopy_from_memo(selector):
    provider_copy = providers.deepcopy(
        selector,
        memo={id(selector): selector},
    )
    assert provider_copy is selector


def test_deepcopy_overridden(selector):
    object_provider = providers.Object(object())

    selector.override(object_provider)

    provider_copy = providers.deepcopy(selector)
    object_provider_copy = provider_copy.overridden[0]

    assert selector is not provider_copy
    assert isinstance(selector, providers.Selector)

    assert object_provider is not object_provider_copy
    assert isinstance(object_provider_copy, providers.Object)


@mark.parametrize("selector_type", ["sys-streams"])
def test_deepcopy_with_sys_streams(selector, switch):
    provider_copy = providers.deepcopy(selector)

    assert selector is not provider_copy
    assert isinstance(provider_copy, providers.Selector)

    with switch.override("stdin"):
        assert selector() is sys.stdin

    with switch.override("stdout"):
        assert selector() is sys.stdout

    with switch.override("stderr"):
        assert selector() is sys.stderr


def test_repr(selector, switch):
    assert "<dependency_injector.providers.Selector({0}".format(repr(switch)) in repr(selector)
    assert "one={0}".format(repr(selector.one)) in repr(selector)
    assert "two={0}".format(repr(selector.two)) in repr(selector)
    assert "at {0}".format(hex(id(selector))) in repr(selector)
