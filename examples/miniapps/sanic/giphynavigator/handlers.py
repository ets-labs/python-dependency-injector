"""Handlers module."""

from sanic.request import Request
from sanic.response import HTTPResponse, json
from dependency_injector.wiring import inject, Provide

from .services import SearchService
from .containers import Container


@inject
async def index(
        request: Request,
        search_service: SearchService = Provide[Container.search_service],
        default_query: str = Provide[Container.config.default.query],
        default_limit: int = Provide[Container.config.default.limit.as_int()],
) -> HTTPResponse:
    query = request.args.get("query", default_query)
    limit = int(request.args.get("limit", default_limit))

    gifs = await search_service.search(query, limit)

    return json(
        {
            "query": query,
            "limit": limit,
            "gifs": gifs,
        },
    )
