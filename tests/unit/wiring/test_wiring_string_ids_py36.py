import contextlib
from decimal import Decimal
import importlib
import unittest

from dependency_injector.wiring import (
    wire,
    Provide,
    Provider,
    Closing,
    register_loader_containers,
    unregister_loader_containers,
)
from dependency_injector import containers, providers, errors

# Runtime import to avoid syntax errors in samples on Python < 3.5
import os
_TOP_DIR = os.path.abspath(
    os.path.sep.join((
        os.path.dirname(__file__),
        '../',
    )),
)
_SAMPLES_DIR = os.path.abspath(
    os.path.sep.join((
        os.path.dirname(__file__),
        '../samples/',
    )),
)
import sys
sys.path.append(_TOP_DIR)
sys.path.append(_SAMPLES_DIR)

from asyncutils import AsyncTestCase

from wiringstringidssamples import module, package
from wiringstringidssamples.service import Service
from wiringstringidssamples.container import Container, SubContainer


class WiringTest(unittest.TestCase):

    container: Container

    def setUp(self) -> None:
        self.container = Container(config={'a': {'b': {'c': 10}}})
        self.container.wire(
            modules=[module],
            packages=[package],
        )
        self.addCleanup(self.container.unwire)

    def test_package_lookup(self):
        from wiringstringidssamples.package import test_package_function
        service = test_package_function()
        self.assertIsInstance(service, Service)

    def test_package_subpackage_lookup(self):
        from wiringstringidssamples.package.subpackage import test_package_function
        service = test_package_function()
        self.assertIsInstance(service, Service)

    def test_package_submodule_lookup(self):
        from wiringstringidssamples.package.subpackage.submodule import test_function
        service = test_function()
        self.assertIsInstance(service, Service)

    def test_module_attributes_wiring(self):
        self.assertIsInstance(module.service, Service)
        self.assertIsInstance(module.service_provider(), Service)
        self.assertIsInstance(module.undefined, Provide)

    def test_class_wiring(self):
        test_class_object = module.TestClass()
        self.assertIsInstance(test_class_object.service, Service)

    def test_class_wiring_context_arg(self):
        test_service = self.container.service()

        test_class_object = module.TestClass(service=test_service)
        self.assertIs(test_class_object.service, test_service)

    def test_class_method_wiring(self):
        test_class_object = module.TestClass()
        service = test_class_object.method()
        self.assertIsInstance(service, Service)

    def test_class_classmethod_wiring(self):
        service = module.TestClass.class_method()
        self.assertIsInstance(service, Service)

    def test_instance_classmethod_wiring(self):
        instance = module.TestClass()
        service = instance.class_method()
        self.assertIsInstance(service, Service)

    def test_class_staticmethod_wiring(self):
        service = module.TestClass.static_method()
        self.assertIsInstance(service, Service)

    def test_instance_staticmethod_wiring(self):
        instance = module.TestClass()
        service = instance.static_method()
        self.assertIsInstance(service, Service)

    def test_class_attribute_wiring(self):
        self.assertIsInstance(module.TestClass.service, Service)
        self.assertIsInstance(module.TestClass.service_provider(), Service)
        self.assertIsInstance(module.TestClass.undefined, Provide)

    def test_function_wiring(self):
        service = module.test_function()
        self.assertIsInstance(service, Service)

    def test_function_wiring_context_arg(self):
        test_service = self.container.service()

        service = module.test_function(service=test_service)
        self.assertIs(service, test_service)

    def test_function_wiring_provider(self):
        service = module.test_function_provider()
        self.assertIsInstance(service, Service)

    def test_function_wiring_provider_context_arg(self):
        test_service = self.container.service()

        service = module.test_function_provider(service_provider=lambda: test_service)
        self.assertIs(service, test_service)

    def test_configuration_option(self):
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

        self.assertEqual(value_int, 10)
        self.assertEqual(value_float, 10.0)
        self.assertEqual(value_str, '10')
        self.assertEqual(value_decimal, Decimal(10))
        self.assertEqual(value_required, 10)
        self.assertEqual(value_required_int, 10)
        self.assertEqual(value_required_float, 10.0)
        self.assertEqual(value_required_str, '10')
        self.assertEqual(value_required_decimal, Decimal(10))

    def test_configuration_option_required_undefined(self):
        self.container.config.reset_override()
        with self.assertRaisesRegex(errors.Error, 'Undefined configuration option "config.a.b.c"'):
            module.test_config_value_required_undefined()

    def test_provide_provider(self):
        service = module.test_provide_provider()
        self.assertIsInstance(service, Service)

    def test_provided_instance(self):
        class TestService:
            foo = {
                'bar': lambda: 10,
            }

        with self.container.service.override(TestService()):
            some_value = module.test_provided_instance()
        self.assertEqual(some_value, 10)

    def test_subcontainer(self):
        some_value = module.test_subcontainer_provider()
        self.assertEqual(some_value, 1)

    def test_config_invariant(self):
        config = {
            'option': {
                'a': 1,
                'b': 2,
            },
            'switch': 'a',
        }
        self.container.config.from_dict(config)

        value_default = module.test_config_invariant()
        self.assertEqual(value_default, 1)

        with self.container.config.switch.override('a'):
            value_a = module.test_config_invariant()
        self.assertEqual(value_a, 1)

        with self.container.config.switch.override('b'):
            value_b = module.test_config_invariant()
        self.assertEqual(value_b, 2)

    def test_wire_with_class_error(self):
        with self.assertRaises(Exception):
            wire(
                container=Container,
                modules=[module],
            )

    def test_unwire_function(self):
        self.container.unwire()
        self.assertIsInstance(module.test_function(), Provide)

    def test_unwire_class(self):
        self.container.unwire()
        test_class_object = module.TestClass()
        self.assertIsInstance(test_class_object.service, Provide)

    def test_unwire_class_method(self):
        self.container.unwire()
        test_class_object = module.TestClass()
        self.assertIsInstance(test_class_object.method(), Provide)

    def test_unwire_package_function(self):
        self.container.unwire()
        from wiringstringidssamples.package.subpackage.submodule import test_function
        self.assertIsInstance(test_function(), Provide)

    def test_unwire_package_function_by_reference(self):
        from wiringstringidssamples.package.subpackage import submodule
        self.container.unwire()
        self.assertIsInstance(submodule.test_function(), Provide)

    def test_unwire_module_attributes(self):
        self.container.unwire()
        self.assertIsInstance(module.service, Provide)
        self.assertIsInstance(module.service_provider, Provider)
        self.assertIsInstance(module.undefined, Provide)

    def test_unwire_class_attributes(self):
        self.container.unwire()
        self.assertIsInstance(module.TestClass.service, Provide)
        self.assertIsInstance(module.TestClass.service_provider, Provider)
        self.assertIsInstance(module.TestClass.undefined, Provide)

    def test_wire_multiple_containers(self):
        sub_container = SubContainer()
        sub_container.wire(
            modules=[module],
            packages=[package],
        )
        self.addCleanup(sub_container.unwire)

        service, some_value = module.test_provide_from_different_containers()

        self.assertIsInstance(service, Service)
        self.assertEqual(some_value, 1)

    def test_closing_resource(self):
        from wiringstringidssamples import resourceclosing

        resourceclosing.Service.reset_counter()

        container = resourceclosing.Container()
        container.wire(modules=[resourceclosing])
        self.addCleanup(container.unwire)

        result_1 = resourceclosing.test_function()
        self.assertIsInstance(result_1, resourceclosing.Service)
        self.assertEqual(result_1.init_counter, 1)
        self.assertEqual(result_1.shutdown_counter, 1)

        result_2 = resourceclosing.test_function()
        self.assertIsInstance(result_2, resourceclosing.Service)
        self.assertEqual(result_2.init_counter, 2)
        self.assertEqual(result_2.shutdown_counter, 2)

        self.assertIsNot(result_1, result_2)

    def test_closing_resource_context(self):
        from wiringstringidssamples import resourceclosing

        resourceclosing.Service.reset_counter()
        service = resourceclosing.Service()

        container = resourceclosing.Container()
        container.wire(modules=[resourceclosing])
        self.addCleanup(container.unwire)

        result_1 = resourceclosing.test_function(service=service)
        self.assertIs(result_1, service)
        self.assertEqual(result_1.init_counter, 0)
        self.assertEqual(result_1.shutdown_counter, 0)

        result_2 = resourceclosing.test_function(service=service)
        self.assertIs(result_2, service)
        self.assertEqual(result_2.init_counter, 0)
        self.assertEqual(result_2.shutdown_counter, 0)

    def test_class_decorator(self):
        service = module.test_class_decorator()
        self.assertIsInstance(service, Service)

    def test_container(self):
        service = module.test_container()
        self.assertIsInstance(service, Service)


class WiringAndFastAPITest(unittest.TestCase):

    container: Container

    def test_bypass_marker_injection(self):
        container = Container()
        container.wire(modules=[module])
        self.addCleanup(container.unwire)

        service = module.test_function(service=Provide[Container.service])
        self.assertIsInstance(service, Service)

    def test_closing_resource_bypass_marker_injection(self):
        from wiringstringidssamples import resourceclosing

        resourceclosing.Service.reset_counter()

        container = resourceclosing.Container()
        container.wire(modules=[resourceclosing])
        self.addCleanup(container.unwire)

        result_1 = resourceclosing.test_function(
            service=Closing[Provide[resourceclosing.Container.service]],
        )
        self.assertIsInstance(result_1, resourceclosing.Service)
        self.assertEqual(result_1.init_counter, 1)
        self.assertEqual(result_1.shutdown_counter, 1)

        result_2 = resourceclosing.test_function(
            service=Closing[Provide[resourceclosing.Container.service]],
        )
        self.assertIsInstance(result_2, resourceclosing.Service)
        self.assertEqual(result_2.init_counter, 2)
        self.assertEqual(result_2.shutdown_counter, 2)

        self.assertIsNot(result_1, result_2)


class WireDynamicContainerTest(unittest.TestCase):

    def test_wire(self):
        sub = containers.DynamicContainer()
        sub.int_object = providers.Object(1)

        container = containers.DynamicContainer()
        container.config = providers.Configuration()
        container.service = providers.Factory(Service)
        container.sub = sub

        container.wire(
            modules=[module],
            packages=[package],
        )
        self.addCleanup(container.unwire)

        service = module.test_function()
        self.assertIsInstance(service, Service)


class WiringAsyncInjectionsTest(AsyncTestCase):

    def test_async_injections(self):
        from wiringstringidssamples import asyncinjections

        container = asyncinjections.Container()
        container.wire(modules=[asyncinjections])
        self.addCleanup(container.unwire)

        asyncinjections.resource1.reset_counters()
        asyncinjections.resource2.reset_counters()

        resource1, resource2 = self._run(asyncinjections.async_injection())

        self.assertIs(resource1, asyncinjections.resource1)
        self.assertEqual(asyncinjections.resource1.init_counter, 1)
        self.assertEqual(asyncinjections.resource1.shutdown_counter, 0)

        self.assertIs(resource2, asyncinjections.resource2)
        self.assertEqual(asyncinjections.resource2.init_counter, 1)
        self.assertEqual(asyncinjections.resource2.shutdown_counter, 0)

    def test_async_injections_with_closing(self):
        from wiringstringidssamples import asyncinjections

        container = asyncinjections.Container()
        container.wire(modules=[asyncinjections])
        self.addCleanup(container.unwire)

        asyncinjections.resource1.reset_counters()
        asyncinjections.resource2.reset_counters()

        resource1, resource2 = self._run(asyncinjections.async_injection_with_closing())

        self.assertIs(resource1, asyncinjections.resource1)
        self.assertEqual(asyncinjections.resource1.init_counter, 1)
        self.assertEqual(asyncinjections.resource1.shutdown_counter, 1)

        self.assertIs(resource2, asyncinjections.resource2)
        self.assertEqual(asyncinjections.resource2.init_counter, 1)
        self.assertEqual(asyncinjections.resource2.shutdown_counter, 1)

        resource1, resource2 = self._run(asyncinjections.async_injection_with_closing())

        self.assertIs(resource1, asyncinjections.resource1)
        self.assertEqual(asyncinjections.resource1.init_counter, 2)
        self.assertEqual(asyncinjections.resource1.shutdown_counter, 2)

        self.assertIs(resource2, asyncinjections.resource2)
        self.assertEqual(asyncinjections.resource2.init_counter, 2)
        self.assertEqual(asyncinjections.resource2.shutdown_counter, 2)


class AutoLoaderTest(unittest.TestCase):

    container: Container

    def setUp(self) -> None:
        self.container = Container(config={'a': {'b': {'c': 10}}})
        importlib.reload(module)

    def tearDown(self) -> None:
        with contextlib.suppress(ValueError):
            unregister_loader_containers(self.container)

        self.container.unwire()

    @classmethod
    def tearDownClass(cls) -> None:
        importlib.reload(module)

    def test_register_container(self):
        register_loader_containers(self.container)
        importlib.reload(module)

        service = module.test_function()
        self.assertIsInstance(service, Service)
