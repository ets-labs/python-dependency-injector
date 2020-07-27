"""Views module."""

from aiohttp import web

from .services import SearchService


async def index(
        request: web.Request,
        search_service: SearchService,
        default_query: str,
        default_limit: int,
) -> web.Response:
    query = request.query.get('query', default_query)
    limit = request.query.get('limit', default_limit)

    gifs = await search_service.search(query, limit)

    return web.json_response(
        {
            'query': query,
            'limit': limit,
            'gifs': gifs,
        },
    )
