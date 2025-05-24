"""The module responsible for verifying user subscriptions."""
from logging import getLogger
from typing import List, Tuple

from aiogram import Bot
from aiogram.exceptions import TelegramNotFound
from aiogram.types import (
    ChatFullInfo,
    ChatMember,
    ChatMemberAdministrator,
    ChatMemberMember,
    ChatMemberOwner,
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


async def check_subscription_on_channels(
    user_id: int, bot: Bot, channels: List[str]
) -> List[str]:
    """
    Check the user's subscriptions for each channel.

    The function returns a list of channel IDs that the user is not subscribed to.
    :param user_id: User ID.
    :param bot: Bot object.
    :param channels: List of channel IDs.
    :return: A list of channel IDs that the user is not subscribed to.
    If the list is empty, then the user is subscribed to all channels.
    """
    logger.debug("Check user subscription on channels: %s", str(channels))
    without_subscription: List[str] = list()

    for channel_id in channels:
        try:
            if await subscription_verification(user_id, bot, channel_id):
                without_subscription.append(channel_id)
        except TelegramNotFound as exc:
            logger.error("User or chat not found. %s", str(exc))

    return without_subscription


async def get_channel_title_and_url(
    channel_id: str, bot: Bot
) -> Tuple[str, str]:
    """Return channel title and url."""
    channel: ChatFullInfo = await bot.get_chat(channel_id)
    title: str = channel.title
    if channel.username:
        url: str = f"https://t.me/{channel.username}"
    else:
        url = f"https://t.me/{channel_id}"

    logger.debug("Chat info: id: %s; title: %s; username: %s; url: %s")
    return title, url
