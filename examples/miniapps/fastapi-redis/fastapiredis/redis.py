from typing import AsyncIterator

from aioredis import from_url, Redis


async def init_redis_pool(host: str, password: str) -> AsyncIterator[Redis]:
    session = from_url(f"redis://{host}", encoding="utf-8", password=password, decode_responses=True)
    yield session
    session.close()
    await session.wait_closed()
