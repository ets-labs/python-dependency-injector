from httpx import AsyncClient

# Runtime import to avoid syntax errors in samples on Python < 3.5 and reach top-dir
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

from wiringfastapi import web


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
