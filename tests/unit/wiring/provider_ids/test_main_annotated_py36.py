"""Main wiring tests for Annotated attribute and argument injection."""

from decimal import Decimal
import typing

from dependency_injector import errors
from dependency_injector.wiring import Closing, Provide, Provider, wire
from pytest import fixture, mark, raises

from samples.wiring import module_annotated as module, package, resourceclosing
from samples.wiring.service import Service
from samples.wiring.container import Container, SubContainer

@fixture(autouse=True)
def container():
    container = Container(config={"a": {"b": {"c": 10}}})
    container.wire(
        modules=[module],
        packages=[package],
    )
    yield container
    container.unwire()

@fixture
def subcontainer():
    container = SubContainer()
    container.wire(
        modules=[module],
        packages=[package],
    )
    yield container
    container.unwire()

@fixture
def resourceclosing_container():
    container = resourceclosing.Container()
    container.wire(modules=[resourceclosing])
    yield container
    container.unwire()

def test_module_attributes_wiring():
    assert isinstance(module.service, Service)
    assert isinstance(module.service_provider(), Service)
    assert isinstance(module.__annotations__['undefined'], typing._AnnotatedAlias)

def test_class_wiring():
    test_class_object = module.TestClass()
    assert isinstance(test_class_object.service, Service)

def test_class_wiring_context_arg(container: Container):
    test_service = container.service()
    test_class_object = module.TestClass(service=test_service)
    assert test_class_object.service is test_service

def test_class_method_wiring():
    test_class_object = module.TestClass()
    service = test_class_object.method()
    assert isinstance(service, Service)

def test_class_classmethod_wiring():
    service = module.TestClass.class_method()
    assert isinstance(service, Service)

def test_instance_classmethod_wiring():
    instance = module.TestClass()
    service = instance.class_method()
    assert isinstance(service, Service)

def test_class_staticmethod_wiring():
    service = module.TestClass.static_method()
    assert isinstance(service, Service)

def test_instance_staticmethod_wiring():
    instance = module.TestClass()
    service = instance.static_method()
    assert isinstance(service, Service)

def test_class_attribute_wiring():
    assert isinstance(module.TestClass.service, Service)
    assert isinstance(module.TestClass.service_provider(), Service)
    assert isinstance(module.TestClass.__annotations__['undefined'], typing._AnnotatedAlias)

def test_function_wiring():
    service = module.test_function()
    assert isinstance(service, Service)

def test_function_wiring_context_arg(container: Container):
    test_service = container.service()
    service = module.test_function(service=test_service)
    assert service is test_service

def test_function_wiring_provider():
    service = module.test_function_provider()
    assert isinstance(service, Service)

def test_function_wiring_provider_context_arg(container: Container):
    test_service = container.service()
    service = module.test_function_provider(service_provider=lambda: test_service)
    assert service is test_service

def test_configuration_option():
    (
        value_int,
        value_float,
        value_str,
        value_decimal,
        value_required,
        value_required_int,
        value_required_float,
        value_required_str,
        value_required_decimal,
    ) = module.test_config_value()

    assert value_int == 10
    assert value_float == 10.0
    assert value_str == "10"
    assert value_decimal == Decimal(10)
    assert value_required == 10
    assert value_required_int == 10
    assert value_required_float == 10.0
    assert value_required_str == "10"
    assert value_required_decimal == Decimal(10)

def test_configuration_option_required_undefined(container: Container):
    container.config.reset_override()
    with raises(errors.Error, match="Undefined configuration option \"config.a.b.c\""):
        module.test_config_value_required_undefined()

def test_provide_provider():
    service = module.test_provide_provider()
    assert isinstance(service, Service)

def test_provider_provider():
    service = module.test_provider_provider()
    assert isinstance(service, Service)

def test_provided_instance(container: Container):
    class TestService:
        foo = {"bar": lambda: 10}

    with container.service.override(TestService()):
        some_value = module.test_provided_instance()
    assert some_value == 10

def test_subcontainer():
    some_value = module.test_subcontainer_provider()
    assert some_value == 1

def test_config_invariant(container: Container):
    config = {
        "option": {
            "a": 1,
            "b": 2,
        },
        "switch": "a",
    }
    container.config.from_dict(config)

    value_default = module.test_config_invariant()
    assert value_default == 1

    with container.config.switch.override("a"):
        value_a = module.test_config_invariant()
    assert value_a == 1

    with container.config.switch.override("b"):
        value_b = module.test_config_invariant()
    assert value_b == 2

def test_class_decorator():
    service = module.test_class_decorator()
    assert isinstance(service, Service)

def test_container():
    service = module.test_container()
    assert isinstance(service, Service)
