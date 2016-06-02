"""Overriding of factory provider example."""

from dependency_injector import providers


object_factory = providers.Factory(object)

object_factory.override(providers.Factory(list))

if __name__ == '__main__':
    object1 = object_factory()
    object2 = object_factory()

    assert object1 is not object2
    assert isinstance(object1, list) and isinstance(object2, list)
