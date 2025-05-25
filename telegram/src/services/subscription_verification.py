"""The module responsible for verifying user subscriptions."""

from logging import getLogger
from typing import List, Optional, Set

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import (
    ChatMember,
    ChatMemberAdministrator,
    ChatMemberMember,
    ChatMemberOwner,
)

from repositories.channels_to_subscribe.redis import (
    RedisChannelsToSubscribeRepository,
)
from schemas.channels_to_subscribe import ChannelToSubscribeSchema
from telegram.src.db.repositories.channels_to_subscribe import (
    SQLAlchemyChannelsToSubscribeRepository,
)

logger = getLogger("telegram.services.subscription_verification")


async def subscription_verification(
    user_id: int, bot: Bot, channel_id: str
) -> bool:
    """Check the user's subscription to the channel."""
    logger.debug(
        "Get member with id %d in chat with id %s", user_id, str(channel_id)
    )
    member: ChatMember = await bot.get_chat_member(channel_id, user_id)
    return isinstance(
        member, (ChatMemberMember, ChatMemberAdministrator, ChatMemberOwner)
    )


async def get_channels_to_subscribe(
    redis_channels_repo: RedisChannelsToSubscribeRepository,
    alchemy_channels_repo: SQLAlchemyChannelsToSubscribeRepository,
) -> Set[ChannelToSubscribeSchema]:
    """
    Get channels to subscribe.

    The function first searches for data in redis,
    if it doesn't find it, it searches in postgres (using sqlalchemy).
    If it doesn't find it, it returns an empty set.
    :param redis_channels_repo: redis channels repository.
    :param alchemy_channels_repo: sqlalchemy channels repository.
    :return: Set of channels to subscribe.
    """
    channels: Optional[Set[ChannelToSubscribeSchema]] = (
        await redis_channels_repo.get_all()
    )
    if channels is None:
        channels = await alchemy_channels_repo.get_all()
        if channels is None:
            return set()
        else:
            for channel in channels:
                await redis_channels_repo.add(channel)
    return channels


async def check_subscription_on_channels(
    user_id: int,
    bot: Bot,
    redis_channels_repo: RedisChannelsToSubscribeRepository,
    alchemy_channels_repo: SQLAlchemyChannelsToSubscribeRepository,
) -> List[ChannelToSubscribeSchema]:
    """
    Check the user's subscriptions for each channel.

    The function returns a list of channel IDs that the user is not subscribed to.
    :param user_id: User ID.
    :param bot: Bot object.
    :param redis_channels_repo: channels repository based on redis.
    :param alchemy_channels_repo: channels repository based on sqlalchemy[postgres]
    :return: A List of ChannelToSubscribeSchema that the user is not subscribed to.
    If the list is empty, then the user is subscribed to all channels.
    """
    channels: Set[ChannelToSubscribeSchema] = await get_channels_to_subscribe(
        redis_channels_repo, alchemy_channels_repo
    )
    logger.debug("Check user subscription on channels: %s", str(channels))
    without_subscription: List[ChannelToSubscribeSchema] = list()

    for channel in channels:
        try:
            if not await subscription_verification(user_id, bot, channel.id):
                without_subscription.append(channel)
        except TelegramBadRequest as exc:
            logger.error(str(exc))

    return without_subscription
