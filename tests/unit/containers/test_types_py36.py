"""Container typing in runtime tests."""

from dependency_injector import containers


def test_types_declarative():
    container: containers.Container = containers.DeclarativeContainer()
    assert isinstance(container, containers.Container)


def test_types_dynamic():
    container: containers.Container = containers.DynamicContainer()
    assert isinstance(container, containers.Container)
