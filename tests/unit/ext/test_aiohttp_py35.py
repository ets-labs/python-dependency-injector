"""Dependency injector Aiohttp extension unit tests."""

from aiohttp import web
from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop

from dependency_injector import containers, providers
from dependency_injector.ext import aiohttp


async def index_view(_):
    return web.Response(text="Hello World!")


async def second_view(_):
    return web.Response(text="Test!")


class OtherClassBasedView(web.View):
    async def get(self):
        return web.Response(text="Test class-based!")


@web.middleware
async def middleware(request, handler):
    resp = await handler(request)
    resp.text = resp.text + " wink1"
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
            aiohttp.MiddlewareFactory(middleware_factory, text=" wink2"),
        ),
    )

    index_view = aiohttp.View(index_view)
    second_view = aiohttp.View(second_view)
    other_class_based_view = aiohttp.ClassBasedView(OtherClassBasedView)


class ApplicationTests(AioHTTPTestCase):

    async def get_application(self):
        """
        Override the get_app method to return your application.
        """
        container = ApplicationContainer()
        app = container.app()
        app.container = container
        app.add_routes([
            web.get("/", container.index_view.as_view()),
            web.get("/second", container.second_view.as_view(), name="second"),
            web.get("/class-based", container.other_class_based_view.as_view()),
        ])
        return app

    @unittest_run_loop
    async def test_index(self):
        response = await self.client.get("/")

        self.assertEqual(response.status, 200)
        self.assertEqual(await response.text(), "Hello World! wink2 wink1")

    @unittest_run_loop
    async def test_second(self):
        response = await self.client.get("/second")

        self.assertEqual(response.status, 200)
        self.assertEqual(await response.text(), "Test! wink2 wink1")

    @unittest_run_loop
    async def test_class_based(self):
        response = await self.client.get("/class-based")

        self.assertEqual(response.status, 200)
        self.assertEqual(await response.text(), "Test class-based! wink2 wink1")

    @unittest_run_loop
    async def test_endpoints(self):
        self.assertEqual(str(self.app.router["second"].url_for()), "/second")
