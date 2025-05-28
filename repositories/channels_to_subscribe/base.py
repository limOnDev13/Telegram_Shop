"""The module responsible for the basic repository of subscription channels."""

from abc import ABC, abstractmethod
from typing import Optional, Set

from schemas.channels_to_subscribe import ChannelToSubscribeSchema


class BaseChannelsToSubscribeRepository(ABC):
    """Base channels to subscribe repo."""

    @abstractmethod
    async def add(self, channel_schema: ChannelToSubscribeSchema) -> None:
        """Add new channel."""
        pass

    @abstractmethod
    async def get_all(self) -> Optional[Set[ChannelToSubscribeSchema]]:
        """Get all channels."""
        pass

    @abstractmethod
    async def remove(self, channel_id: str) -> None:
        """Remove channel by id."""
        pass

    @abstractmethod
    async def update(
        self, new_channel_schema: ChannelToSubscribeSchema
    ) -> None:
        """Update channel with channel_id."""
        await self.remove(new_channel_schema.id)
        await self.add(new_channel_schema)
