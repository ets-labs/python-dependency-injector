"""Test module for wiring with Annotated."""

import sys
import pytest

if sys.version_info < (3, 9):
    pytest.skip("Annotated is only available in Python 3.9+", allow_module_level=True)

from decimal import Decimal
from typing import Callable, Annotated

from dependency_injector import providers
from dependency_injector.wiring import inject, Provide, Provider

from .container import Container, SubContainer
from .service import Service

service: Annotated[Service, Provide[Container.service]]
service_provider: Annotated[Callable[..., Service], Provider[Container.service]]
undefined: Annotated[Callable, Provide[providers.Provider()]]

class TestClass:
    service: Annotated[Service, Provide[Container.service]]
    service_provider: Annotated[Callable[..., Service], Provider[Container.service]]
    undefined: Annotated[Callable, Provide[providers.Provider()]]

    @inject
    def __init__(self, service: Annotated[Service, Provide[Container.service]]):
        self.service = service

    @inject
    def method(self, service: Annotated[Service, Provide[Container.service]]):
        return service

    @classmethod
    @inject
    def class_method(cls, service: Annotated[Service, Provide[Container.service]]):
        return service

    @staticmethod
    @inject
    def static_method(service: Annotated[Service, Provide[Container.service]]):
        return service

@inject
def test_function(service: Annotated[Service, Provide[Container.service]]):
    return service

@inject
def test_function_provider(service_provider: Annotated[Callable[..., Service], Provider[Container.service]]):
    service = service_provider()
    return service

@inject
def test_config_value(
        value_int: Annotated[int, Provide[Container.config.a.b.c.as_int()]],
        value_float: Annotated[float, Provide[Container.config.a.b.c.as_float()]],
        value_str: Annotated[str, Provide[Container.config.a.b.c.as_(str)]],
        value_decimal: Annotated[Decimal, Provide[Container.config.a.b.c.as_(Decimal)]],
        value_required: Annotated[str, Provide[Container.config.a.b.c.required()]],
        value_required_int: Annotated[int, Provide[Container.config.a.b.c.required().as_int()]],
        value_required_float: Annotated[float, Provide[Container.config.a.b.c.required().as_float()]],
        value_required_str: Annotated[str, Provide[Container.config.a.b.c.required().as_(str)]],
        value_required_decimal: Annotated[str, Provide[Container.config.a.b.c.required().as_(Decimal)]],
):
    return (
        value_int,
        value_float,
        value_str,
        value_decimal,
        value_required,
        value_required_int,
        value_required_float,
        value_required_str,
        value_required_decimal,
    )

@inject
def test_config_value_required_undefined(
        value_required: Annotated[int, Provide[Container.config.a.b.c.required()]],
):
    return value_required

@inject
def test_provide_provider(service_provider: Annotated[Callable[..., Service], Provide[Container.service.provider]]):
    service = service_provider()
    return service

@inject
def test_provider_provider(service_provider: Annotated[Callable[..., Service], Provider[Container.service.provider]]):
    service = service_provider()
    return service

@inject
def test_provided_instance(some_value: Annotated[int, Provide[Container.service.provided.foo["bar"].call()]]):
    return some_value

@inject
def test_subcontainer_provider(some_value: Annotated[int, Provide[Container.sub.int_object]]):
    return some_value

@inject
def test_config_invariant(some_value: Annotated[int, Provide[Container.config.option[Container.config.switch]]]):
    return some_value

@inject
def test_provide_from_different_containers(
        service: Annotated[Service, Provide[Container.service]],
        some_value: Annotated[int, Provide[SubContainer.int_object]],
):
    return service, some_value

class ClassDecorator:
    def __init__(self, fn):
        self._fn = fn

    def __call__(self, *args, **kwargs):
        return self._fn(*args, **kwargs)

@ClassDecorator
@inject
def test_class_decorator(service: Annotated[Service, Provide[Container.service]]):
    return service

def test_container(container: Annotated[Container, Provide[Container]]):
    return container.service()
