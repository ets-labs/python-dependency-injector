"""Aiohttp extension tests."""

from aiohttp import web, test_utils
from dependency_injector import containers, providers
from dependency_injector.ext import aiohttp
from pytest import fixture, mark


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


@fixture
def app():
    container = ApplicationContainer()
    app = container.app()
    app.container = container
    app.add_routes([
        web.get("/", container.index_view.as_view()),
        web.get("/second", container.second_view.as_view(), name="second"),
        web.get("/class-based", container.other_class_based_view.as_view()),
    ])
    return app


@fixture
async def client(app):
    async with test_utils.TestClient(test_utils.TestServer(app)) as client:
        yield client


@mark.asyncio
@mark.filterwarnings("ignore:The loop argument is deprecated:DeprecationWarning")
async def test_index(client):
    response = await client.get("/")

    assert response.status == 200
    assert await response.text() == "Hello World! wink2 wink1"


@mark.asyncio
@mark.filterwarnings("ignore:The loop argument is deprecated:DeprecationWarning")
async def test_second(client):
    response = await client.get("/second")

    assert response.status == 200
    assert await response.text() == "Test! wink2 wink1"


@mark.asyncio
@mark.filterwarnings("ignore:The loop argument is deprecated:DeprecationWarning")
async def test_class_based(client):
    response = await client.get("/class-based")

    assert response.status == 200
    assert await response.text() == "Test class-based! wink2 wink1"


def test_endpoints(app):
    assert str(app.router["second"].url_for()) == "/second"
