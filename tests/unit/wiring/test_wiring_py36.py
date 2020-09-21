from decimal import Decimal
import unittest

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
