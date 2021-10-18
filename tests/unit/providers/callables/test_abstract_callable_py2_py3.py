"""AbstractCallable provider tests."""

from dependency_injector import providers, errors
from pytest import raises

from .common import example


def test_inheritance():
    assert isinstance(providers.AbstractCallable(example), providers.Callable)


def test_call_overridden_by_callable():
    def _abstract_example():
        pass

    provider = providers.AbstractCallable(_abstract_example)
    provider.override(providers.Callable(example))

    assert provider(1, 2, 3, 4) == (1, 2, 3, 4)


def test_call_overridden_by_delegated_callable():
    def _abstract_example():
        pass

    provider = providers.AbstractCallable(_abstract_example)
    provider.override(providers.DelegatedCallable(example))

    assert provider(1, 2, 3, 4) == (1, 2, 3, 4)


def test_call_not_overridden():
    provider = providers.AbstractCallable(example)
    with raises(errors.Error):
        provider(1, 2, 3, 4)


def test_override_by_not_callable():
    provider = providers.AbstractCallable(example)
    with raises(errors.Error):
        provider.override(providers.Factory(object))


def test_provide_not_implemented():
    provider = providers.AbstractCallable(example)
    with raises(NotImplementedError):
        provider._provide((1, 2, 3, 4), dict())


def test_repr():
    provider = providers.AbstractCallable(example)
    assert repr(provider) == (
        "<dependency_injector.providers."
        "AbstractCallable({0}) at {1}>".format(repr(example), hex(id(provider)))
    )
