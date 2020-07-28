"""Dependency injector Aiohttp extension unit tests."""

from aiohttp import web
from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop

from dependency_injector import containers, providers
from dependency_injector.ext import aiohttp


async def index(_):
    return web.Response(text='Hello World!')


async def test(_):
    return web.Response(text='Test!')


class Test(web.View):
    async def get(self):
        return web.Response(text='Test class-based!')


@web.middleware
async def middleware(request, handler):
    resp = await handler(request)
    resp.text = resp.text + ' wink1'
    return resp


def middleware_factory(text):
    @web.middleware
    async def sample_middleware(request, handler):
        resp = await handler(request)
        resp.text = resp.text + text
        return resp
    return sample_middleware


class ApplicationContainer(containers.DeclarativeContainer):

    app = aiohttp.Application(
        web.Application,
        middlewares=providers.List(
            aiohttp.Middleware(middleware),
            aiohttp.MiddlewareFactory(middleware_factory, text=' wink2'),
        ),
    )

    index_view = aiohttp.View(index)
    test_view = aiohttp.View(test)
    test_class_view = aiohttp.ClassBasedView(Test)


class ApplicationTests(AioHTTPTestCase):

    async def get_application(self):
        """
        Override the get_app method to return your application.
        """
        container = ApplicationContainer()
        app = container.app()
        app.container = container
        app.add_routes([
            web.get('/', container.index_view.as_view()),
            web.get('/test', container.test_view.as_view(), name='test'),
            web.get('/test-class', container.test_class_view.as_view()),
        ])
        return app

    @unittest_run_loop
    async def test_index(self):
        response = await self.client.get('/')

        self.assertEqual(response.status, 200)
        self.assertEqual(await response.text(), 'Hello World! wink2 wink1')

    @unittest_run_loop
    async def test_test(self):
        response = await self.client.get('/test')

        self.assertEqual(response.status, 200)
        self.assertEqual(await response.text(), 'Test! wink2 wink1')

    @unittest_run_loop
    async def test_test_class_based(self):
        response = await self.client.get('/test-class')

        self.assertEqual(response.status, 200)
        self.assertEqual(await response.text(), 'Test class-based! wink2 wink1')

    @unittest_run_loop
    async def test_endpoints(self):
        self.assertEqual(str(self.app.router['test'].url_for()), '/test')
