import unittest

from dependency_injector.wiring import (
    Provide,
    Closing,
)
from dependency_injector import containers, errors

# Runtime import to avoid syntax errors in samples on Python < 3.5
import os
_TOP_DIR = os.path.abspath(
    os.path.sep.join((
        os.path.dirname(__file__),
        "../",
    )),
)
_SAMPLES_DIR = os.path.abspath(
    os.path.sep.join((
        os.path.dirname(__file__),
        "../samples/",
    )),
)
import sys
sys.path.append(_TOP_DIR)
sys.path.append(_SAMPLES_DIR)

from wiringsamples import module
from wiringsamples.service import Service
from wiringsamples.container import Container


class ModuleAsPackageTest(unittest.TestCase):

    def setUp(self):
        self.container = Container(config={"a": {"b": {"c": 10}}})
        self.addCleanup(self.container.unwire)

    def test_module_as_package_wiring(self):
        # See: https://github.com/ets-labs/python-dependency-injector/issues/481
        self.container.wire(packages=[module])
        self.assertIsInstance(module.service, Service)


class WiringAndQueue(unittest.TestCase):

    def test_wire_queue(self) -> None:
        from wiringsamples import queuemodule
        container = Container()
        self.addCleanup(container.unwire)

        # Should not raise exception
        # See: https://github.com/ets-labs/python-dependency-injector/issues/362
        try:
            container.wire(modules=[queuemodule])
        except:
            raise


class WiringAndFastAPITest(unittest.TestCase):

    container: Container

    def test_bypass_marker_injection(self):
        container = Container()
        container.wire(modules=[module])
        self.addCleanup(container.unwire)

        service = module.test_function(service=Provide[Container.service])
        self.assertIsInstance(service, Service)

    def test_closing_resource_bypass_marker_injection(self):
        from wiringsamples import resourceclosing

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
