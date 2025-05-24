"""The module responsible for the handles, responsible for starting the dialog."""
from logging import getLogger
from typing import List

from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from telegram.src.config.app import Config
from telegram.src.keyboards import (
    build_kb_with_channels_to_subscribe,
    build_kb_with_main_menu,
)
from telegram.src.lexicon.ru import LEXICON_RU
from telegram.src.services.subscription_verification import (
    check_subscription_on_channels,
)

logger = getLogger("telegram.handlers.start_conversation")
router: Router = Router()


@router.message(CommandStart())
async def process_start_command(msg: Message, config: Config) -> None:
    """Process the /start command."""
    # welcome
    logger.debug("Greet the user.")
    await msg.answer(LEXICON_RU["start"])

    # check subscriptions
    logger.debug("Check user subscriptions.")
    await msg.answer(LEXICON_RU["subscription_verification"])
    without_subscription: List[str] = await check_subscription_on_channels(
        user_id=msg.from_user.id,
        bot=msg.bot,
        channels=config.channels_to_subscribe,
    )

    if without_subscription:
        # ask to subscribe
        logger.debug("Ask to subscribe.")
        await msg.answer(
            text=LEXICON_RU["failed_subscription_verification"],
            reply_markup=await build_kb_with_channels_to_subscribe(
                without_subscription, msg.bot
            ),
        )
    else:
        # show main menu
        logger.debug("Show main menu.")
        await msg.answer(
            text=LEXICON_RU["successful_subscription_verification"],
            reply_markup=build_kb_with_main_menu(),
        )


@router.message(Command(commands="show_channel_id"))
async def show_channel_id(msg: Message) -> None:
    """
    Output the ID of the current channel.

    An auxiliary handle to find out the ID of channels and chats in which
    the bot is the admin and in which this handle is twitching.
    The handle can be easily removed.
    """
    logger.debug("Chat ID: %s", str(msg.chat.id))
    await msg.answer(f"Chat ID: {msg.chat.id}")
