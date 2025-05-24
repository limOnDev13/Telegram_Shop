"""The module responsible for the keyboard with subscription channels."""

from logging import getLogger
from typing import List

from aiogram import Bot
from aiogram.exceptions import TelegramNotFound
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from schemas.channels_to_subscribe import ChannelToSubscribeSchema

logger = getLogger("telegram.keyboards.channels_to_subscribe")


async def build_kb_with_channels_to_subscribe(
    channels: List[ChannelToSubscribeSchema],
) -> InlineKeyboardMarkup:
    """Build a keyboard with subscription channels."""
    logger.debug("Create kb with channels to subscribe.")
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

    bts: List[InlineKeyboardButton] = list()
    for channel in channels:
        try:
            bts.append(
                InlineKeyboardButton(text=channel.title, url=channel.url)
            )
        except TelegramNotFound as exc:
            logger.error("User or chat not found. %s", str(exc))

    kb_builder.row(*bts, width=1)

    return kb_builder.as_markup(resize_keyboard=True)
