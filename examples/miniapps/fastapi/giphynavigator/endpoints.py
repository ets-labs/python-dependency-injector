"""Endpoints module."""

from dependency_injector.wiring import Provide

from .containers import Container


async def index(
        query: str = Provide[Container.config.default.query],
        limit: int = Provide[Container.config.default.limit.as_int()],
        search_service=Provide[Container.search_service],
):
    gifs = await search_service.search(query, limit)
    return {
        'query': query,
        'limit': limit,
        'gifs': gifs,
    }
