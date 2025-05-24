"""The package responsible for the SQLAlchemy subscription channel repo."""

from typing import Optional, Sequence, Set

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from repositories.channels_to_subscribe.base import (
    BaseChannelsToSubscribeRepository,
)
from schemas.channels_to_subscribe import ChannelToSubscribeSchema
from telegram.src.db.models.channel_to_subscribe import ChannelToSubscribe


class SQLAlchemyChannelsToSubscribeRepository(
    BaseChannelsToSubscribeRepository
):
    """SQLAlchemy channels to subscribe repo."""

    def __init__(self, session_fabric: async_sessionmaker[AsyncSession]):
        """
        Init class.

        :param session_fabric: async session fabric.
        """
        self.__session_fabric = session_fabric

    async def add(self, channel_schema: ChannelToSubscribeSchema) -> None:
        """Add new channel."""
        async with self.__session_fabric() as session:
            channel_model = ChannelToSubscribe(**channel_schema.model_dump())
            session.add(channel_model)
            await session.commit()

    async def get_all(self) -> Optional[Set[ChannelToSubscribeSchema]]:
        """Get all channels."""
        async with self.__session_fabric() as session:
            channels_q = await session.execute(select(ChannelToSubscribe))
            channels: Sequence[ChannelToSubscribe] = channels_q.scalars().all()
            return {
                ChannelToSubscribeSchema.model_validate(channel)
                for channel in channels
            }

    async def remove(self, channel_id: str) -> None:
        """Remove channel by id."""
        async with self.__session_fabric() as session:
            channel_q = await session.execute(
                select(ChannelToSubscribe)
                .where(ChannelToSubscribe.id == channel_id)
                .with_for_update()
            )
            channel: Optional[ChannelToSubscribe] = channel_q.first()
            if channel:
                await session.delete(channel)
                await session.commit()

    async def update(
        self, new_channel_schema: ChannelToSubscribeSchema
    ) -> None:
        """Update channel with channel_id."""
        async with self.__session_fabric() as session:
            channel_q = await session.execute(
                select(ChannelToSubscribe)
                .where(ChannelToSubscribe.id == new_channel_schema.id)
                .with_for_update()
            )
            channel: Optional[ChannelToSubscribe] = channel_q.first()
            if channel:
                channel = ChannelToSubscribe(**new_channel_schema.model_dump())
                await session.merge(channel)
                await session.commit()
