"""Container schema fixtures."""

from dependency_injector import containers
from pytest import fixture


@fixture
def container():
    return containers.DynamicContainer()
