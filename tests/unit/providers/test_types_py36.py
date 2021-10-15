"""Provider typing in runtime tests."""

from dependency_injector import providers


class SomeClass:
    ...


def test_provider():
    provider: providers.Provider[SomeClass] = providers.Factory(SomeClass)
    some_object = provider()
    assert isinstance(some_object, SomeClass)
