"""The module responsible for the subscription channel repo, based on redis."""

import json
from typing import List, Optional, Set

from schemas.channels_to_subscribe import ChannelToSubscribeSchema
from utils.redis.mixins import RedisMixin

from .base import BaseChannelsToSubscribeRepository


class RedisChannelsToSubscribeRepository(
    BaseChannelsToSubscribeRepository, RedisMixin
):
    """Redis channels tp subscribe repo."""

    __redis_key: str = "channels_to_subscribe"

    async def add(self, channel_schema: ChannelToSubscribeSchema) -> None:
        """Add new channel."""
        async with self.get_redis_conn() as redis_client:
            await redis_client.hset(
                self.__redis_key,
                channel_schema.id,
                channel_schema.model_dump_json(),
            )

    async def get_all(self) -> Optional[Set[ChannelToSubscribeSchema]]:
        """Get all channels."""
        async with self.get_redis_conn() as redis_client:
            channels: List[str] = await redis_client.hvals(self.__redis_key)
            return {
                ChannelToSubscribeSchema(**json.loads(channel))
                for channel in set(channels)
            }

    async def remove(self, channel_id: str) -> None:
        """Remove channel by id."""
        async with self.get_redis_conn() as redis_client:
            await redis_client.hdel(self.__redis_key, channel_id)

    async def update(
        self, new_channel_schema: ChannelToSubscribeSchema
    ) -> None:
        """Update channel with channel_id."""
        await self.add(new_channel_schema)
