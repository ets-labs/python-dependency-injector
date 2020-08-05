"""Http client module."""

from aiohttp import ClientSession, ClientResponse


class HttpClient:

    async def request(self, method: str, url: str) -> ClientResponse:
        async with ClientSession() as session:
            async with session.request(method, url) as response:
                return response
