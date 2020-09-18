"""Test module for wiring."""

from dependency_injector.wiring import ConfigurationOption


class TestClass:

    def __init__(self, service):
        self.service = service


def test_function(service):
    return service


def test_function_provider(service_provider):
    return service_provider()


def test_config_value(
        some_value_int: int = ConfigurationOption['a.b.c'],
        some_value_str: str = ConfigurationOption['a.b.c'],
):
    return some_value_int, some_value_str
