"""Giphy client module."""

from aiohttp import ClientSession, ClientTimeout


class GiphyClient:

    API_URL = "https://api.giphy.com/v1"

    def __init__(self, api_key, timeout):
        self._api_key = api_key
        self._timeout = ClientTimeout(timeout)

    async def search(self, query, limit):
        """Make search API call and return result."""
        url = f"{self.API_URL}/gifs/search"
        params = {
            "q": query,
            "api_key": self._api_key,
            "limit": limit,
        }
        async with ClientSession(timeout=self._timeout) as session:
            async with session.get(url, params=params) as response:
                if response.status != 200:
                    response.raise_for_status()
                return await response.json()
