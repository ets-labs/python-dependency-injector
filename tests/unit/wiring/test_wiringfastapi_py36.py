import asyncio
import contextlib
import gc
import unittest
from unittest import mock

from httpx import AsyncClient

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

from wiringfastapi import web


# TODO: Refactor to use common async test case
def setup_test_loop(
        loop_factory=asyncio.new_event_loop
) -> asyncio.AbstractEventLoop:
    loop = loop_factory()
    try:
        module = loop.__class__.__module__
        skip_watcher = 'uvloop' in module
    except AttributeError:  # pragma: no cover
        # Just in case
        skip_watcher = True
    asyncio.set_event_loop(loop)
    if sys.platform != "win32" and not skip_watcher:
        policy = asyncio.get_event_loop_policy()
        watcher = asyncio.SafeChildWatcher()  # type: ignore
        watcher.attach_loop(loop)
        with contextlib.suppress(NotImplementedError):
            policy.set_child_watcher(watcher)
    return loop


def teardown_test_loop(loop: asyncio.AbstractEventLoop,
                       fast: bool=False) -> None:
    closed = loop.is_closed()
    if not closed:
        loop.call_soon(loop.stop)
        loop.run_forever()
        loop.close()

    if not fast:
        gc.collect()

    asyncio.set_event_loop(None)


class AsyncTestCase(unittest.TestCase):

    def setUp(self):
        self.loop = setup_test_loop()

    def tearDown(self):
        teardown_test_loop(self.loop)

    def _run(self, f):
        return self.loop.run_until_complete(f)


class WiringFastAPITest(AsyncTestCase):

    client: AsyncClient

    def setUp(self) -> None:
        super().setUp()
        self.client = AsyncClient(app=web.app, base_url='http://test')

    def tearDown(self) -> None:
        self._run(self.client.aclose())
        super().tearDown()

    def test_depends_marker_injection(self):
        class ServiceMock:
            async def process(self):
                return 'Foo'

        with web.container.service.override(ServiceMock()):
            response = self._run(self.client.get('/'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'result': 'Foo'})

    def test_depends_injection(self):
        response = self._run(self.client.get('/auth', auth=('john_smith', 'secret')))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'username': 'john_smith', 'password': 'secret'})
