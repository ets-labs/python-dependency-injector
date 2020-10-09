from decimal import Decimal
import unittest

from dependency_injector.wiring import wire, Provide

from . import module, package
from .service import Service
from .container import Container


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
        from .package.subpackage.submodule import test_function
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
        from .package.subpackage.submodule import test_function
        self.assertIsInstance(test_function(), Provide)

    def test_unwire_package_function_by_reference(self):
        from .package.subpackage import submodule
        self.container.unwire()
        self.assertIsInstance(submodule.test_function(), Provide)
