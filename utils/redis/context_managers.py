"""The module responsible for context managers based on Redis."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from redis.asyncio import Redis


@asynccontextmanager
async def redis_conn(
    redis_url: str,
) -> AsyncGenerator[Redis, None]:
    """
    Yield redis client.

    Async context manager.
    """
    redis_client = Redis.from_url(redis_url)
    try:
        yield redis_client
    finally:
        await redis_client.close()
