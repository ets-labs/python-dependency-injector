"""Dependency injector dynamic container unit tests for async resources."""

import unittest2 as unittest

# Runtime import to get asyncutils module
import os
_TOP_DIR = os.path.abspath(
    os.path.sep.join((
        os.path.dirname(__file__),
        '../',
    )),
)
import sys
sys.path.append(_TOP_DIR)

from asyncutils import AsyncTestCase

from dependency_injector import (
    containers,
    providers,
)


class AsyncResourcesTest(AsyncTestCase):

    @unittest.skipIf(sys.version_info[:2] <= (3, 5), 'Async test')
    def test_async_init_resources(self):
        async def _init1():
            _init1.init_counter += 1
            yield
            _init1.shutdown_counter += 1

        _init1.init_counter = 0
        _init1.shutdown_counter = 0

        async def _init2():
            _init2.init_counter += 1
            yield
            _init2.shutdown_counter += 1

        _init2.init_counter = 0
        _init2.shutdown_counter = 0

        class Container(containers.DeclarativeContainer):
            resource1 = providers.Resource(_init1)
            resource2 = providers.Resource(_init2)

        container = Container()
        self.assertEqual(_init1.init_counter, 0)
        self.assertEqual(_init1.shutdown_counter, 0)
        self.assertEqual(_init2.init_counter, 0)
        self.assertEqual(_init2.shutdown_counter, 0)

        self._run(container.init_resources())
        self.assertEqual(_init1.init_counter, 1)
        self.assertEqual(_init1.shutdown_counter, 0)
        self.assertEqual(_init2.init_counter, 1)
        self.assertEqual(_init2.shutdown_counter, 0)

        self._run(container.shutdown_resources())
        self.assertEqual(_init1.init_counter, 1)
        self.assertEqual(_init1.shutdown_counter, 1)
        self.assertEqual(_init2.init_counter, 1)
        self.assertEqual(_init2.shutdown_counter, 1)

        self._run(container.init_resources())
        self._run(container.shutdown_resources())
        self.assertEqual(_init1.init_counter, 2)
        self.assertEqual(_init1.shutdown_counter, 2)
        self.assertEqual(_init2.init_counter, 2)
        self.assertEqual(_init2.shutdown_counter, 2)
