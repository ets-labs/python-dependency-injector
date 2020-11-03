from decimal import Decimal
import unittest

from dependency_injector.wiring import wire, Provide

# Runtime import to avoid syntax errors in samples on Python < 3.5
import os
_SAMPLES_DIR = os.path.abspath(
    os.path.sep.join((
        os.path.dirname(__file__),
        '../samples/',
    )),
)
import sys
sys.path.append(_SAMPLES_DIR)

from wiringsamples import module, package
from wiringsamples.service import Service
from wiringsamples.container import Container, SubContainer


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
        from wiringsamples.package import test_package_function
        service = test_package_function()
        self.assertIsInstance(service, Service)

    def test_package_subpackage_lookup(self):
        from wiringsamples.package.subpackage import test_package_function
        service = test_package_function()
        self.assertIsInstance(service, Service)

    def test_package_submodule_lookup(self):
        from wiringsamples.package.subpackage.submodule import test_function
        service = test_function()
        self.assertIsInstance(service, Service)

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
        int_value, str_value, decimal_value = module.test_config_value()
        self.assertEqual(int_value, 10)
        self.assertEqual(str_value, '10')
        self.assertEqual(decimal_value, Decimal(10))

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
        from wiringsamples.package.subpackage.submodule import test_function
        self.assertIsInstance(test_function(), Provide)

    def test_unwire_package_function_by_reference(self):
        from wiringsamples.package.subpackage import submodule
        self.container.unwire()
        self.assertIsInstance(submodule.test_function(), Provide)

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
        from wiringsamples import resourceclosing

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
        from wiringsamples import resourceclosing

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
