"""Services module."""

from .giphy import GiphyClient


class SearchService:

    def __init__(self, giphy_client: GiphyClient):
        self._giphy_client = giphy_client

    async def search(self, query, limit):
        """Search for gifs and return formatted data."""
        if not query:
            return []

        result = await self._giphy_client.search(query, limit)

        return [{"url": gif["url"]} for gif in result["data"]]
