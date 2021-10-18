"""Fixtures module."""

from dependency_injector import providers
from pytest import fixture


@fixture
def config_type():
    return "default"


@fixture
def config(config_type):
    if config_type == "strict":
        return providers.Configuration(strict=True)
    elif config_type == "default":
        return providers.Configuration()
    else:
        raise ValueError("Undefined config type \"{0}\"".format(config_type))
