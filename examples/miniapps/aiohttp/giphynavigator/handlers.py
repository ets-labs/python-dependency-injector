"""Handlers module."""

from aiohttp import web
from dependency_injector.wiring import inject, Provide

from .services import SearchService
from .containers import Container


@inject
async def index(
        request: web.Request,
        search_service: SearchService = Provide[Container.search_service],
        default_query: str = Provide[Container.config.default.query],
        default_limit: int = Provide[Container.config.default.limit.as_int()],
) -> web.Response:
    query = request.query.get("query", default_query)
    limit = int(request.query.get("limit", default_limit))

    gifs = await search_service.search(query, limit)

    return web.json_response(
        {
            "query": query,
            "limit": limit,
            "gifs": gifs,
        },
    )
