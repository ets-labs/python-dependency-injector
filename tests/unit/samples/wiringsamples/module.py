"""Test module for wiring."""

from decimal import Decimal
from typing import Callable

from dependency_injector import providers
from dependency_injector.wiring import inject, Provide, Provider

from .container import Container, SubContainer
from .service import Service


service: Service = Provide[Container.service]
service_provider: Callable[..., Service] = Provider[Container.service]
undefined: Callable = Provide[providers.Provider()]


class TestClass:

    service: Service = Provide[Container.service]
    service_provider: Callable[..., Service] = Provider[Container.service]
    undefined: Callable = Provide[providers.Provider()]

    @inject
    def __init__(self, service: Service = Provide[Container.service]):
        self.service = service

    @inject
    def method(self, service: Service = Provide[Container.service]):
        return service

    @classmethod
    @inject
    def class_method(cls, service: Service = Provide[Container.service]):
        return service

    @staticmethod
    @inject
    def static_method(service: Service = Provide[Container.service]):
        return service


@inject
def test_function(service: Service = Provide[Container.service]):
    return service


@inject
def test_function_provider(service_provider: Callable[..., Service] = Provider[Container.service]):
    service = service_provider()
    return service


@inject
def test_config_value(
        value_int: int = Provide[Container.config.a.b.c.as_int()],
        value_float: float = Provide[Container.config.a.b.c.as_float()],
        value_str: str = Provide[Container.config.a.b.c.as_(str)],
        value_decimal: Decimal = Provide[Container.config.a.b.c.as_(Decimal)],
        value_required: str = Provide[Container.config.a.b.c.required()],
        value_required_int: int = Provide[Container.config.a.b.c.required().as_int()],
        value_required_float: float = Provide[Container.config.a.b.c.required().as_float()],
        value_required_str: str = Provide[Container.config.a.b.c.required().as_(str)],
        value_required_decimal: str = Provide[Container.config.a.b.c.required().as_(Decimal)],
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
        value_required: int = Provide[Container.config.a.b.c.required()],
):
    return value_required


@inject
def test_provide_provider(service_provider: Callable[..., Service] = Provider[Container.service.provider]):
    service = service_provider()
    return service


@inject
def test_provided_instance(some_value: int = Provide[Container.service.provided.foo['bar'].call()]):
    return some_value


@inject
def test_subcontainer_provider(some_value: int = Provide[Container.sub.int_object]):
    return some_value


@inject
def test_config_invariant(some_value: int = Provide[Container.config.option[Container.config.switch]]):
    return some_value


@inject
def test_provide_from_different_containers(
        service: Service = Provide[Container.service],
        some_value: int = Provide[SubContainer.int_object],
):
    return service, some_value


class ClassDecorator:
    def __init__(self, fn):
        self._fn = fn

    def __call__(self, *args, **kwargs):
        return self._fn(*args, **kwargs)


@ClassDecorator
@inject
def test_class_decorator(service: Service = Provide[Container.service]):
    return service


def test_container(container: Container = Provide[Container]):
    return container.service()
