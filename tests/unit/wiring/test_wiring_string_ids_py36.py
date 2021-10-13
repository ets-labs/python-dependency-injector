import unittest

from dependency_injector.wiring import (
    Provide,
    Closing,
)
from dependency_injector import containers, providers, errors

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

from wiringstringidssamples import module, package
from wiringstringidssamples.service import Service
from wiringstringidssamples.container import Container


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
