"""Provider utils tests."""

from dependency_injector import providers


def test_with_instance():
    assert providers.is_provider(providers.Provider()) is True


def test_with_class():
    assert providers.is_provider(providers.Provider) is False


def test_with_string():
    assert providers.is_provider("some_string") is False


def test_with_object():
    assert providers.is_provider(object()) is False


def test_with_subclass_instance():
    class SomeProvider(providers.Provider):
        pass

    assert providers.is_provider(SomeProvider()) is True


def test_with_class_with_getattr():
    class SomeClass(object):
        def __getattr__(self, _):
            return False

    assert providers.is_provider(SomeClass()) is False
