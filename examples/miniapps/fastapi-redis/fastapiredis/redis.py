"""Redis client module."""

from typing import AsyncIterator

from aioredis import create_redis_pool, Redis


async def init_redis_pool(host: str, password: str) -> AsyncIterator[Redis]:
    pool = await create_redis_pool(f"redis://{host}", password=password)
    yield pool
    pool.close()
    await pool.wait_closed()
