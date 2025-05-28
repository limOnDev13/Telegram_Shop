"""The module responsible for Redis-based mixins."""

from contextlib import asynccontextmanager
from typing import (
    AsyncGenerator,
    Optional,
    overload,
)

from redis.asyncio import Redis

from .context_managers import redis_conn


class RedisMixin(object):
    """Redis client mixin."""

    @overload
    def __init__(self, redis_client: Redis, redis_url: None = None): ...

    @overload
    def __init__(self, redis_client: None, redis_url: str): ...

    def __init__(
        self,
        redis_client: Optional[Redis] = None,
        redis_url: Optional[str] = None,
    ):
        """
        Init class.

        :param redis_client: Redis client.
        :param redis_url: Redis url
        """
        if redis_client is None and redis_url is None:
            raise ValueError(
                "You need either a redis client or a url to create it."
            )
        self.__redis_client = redis_client
        self.__redis_url = redis_url

    @asynccontextmanager
    async def get_redis_conn(self) -> AsyncGenerator[Redis, None]:
        """Yield redis connection."""
        if self.__redis_client:
            yield self.__redis_client
        elif self.__redis_url:
            async with redis_conn(self.__redis_url) as redis_client:
                yield redis_client
        else:
            raise ValueError("Redis client and redis url are None.")
