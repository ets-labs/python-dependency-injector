"""Services module."""

from aioredis import Redis


class Service:
    def __init__(self, redis: Redis) -> None:
        self._redis = redis

    async def process(self) -> str:
        await self._redis.set("my-key", "value")
        return await self._redis.get("my-key")
