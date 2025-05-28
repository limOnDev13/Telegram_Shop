"""The module responsible for the handles, responsible for starting the dialog."""

from logging import getLogger
from typing import List

from aiogram import F, Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from repositories.channels_to_subscribe.redis import (
    RedisChannelsToSubscribeRepository,
)
from schemas.channels_to_subscribe import ChannelToSubscribeSchema
from telegram.src.config.app import Config
from telegram.src.db.queries.shopping_cart import (
    create_shopping_cart_if_not_exists,
)
from telegram.src.db.repositories import (
    SQLAlchemyChannelsToSubscribeRepository,
)
from telegram.src.keyboards import BACK_TO_MAIN_MENU_CALLBACK
from telegram.src.keyboards.channels_to_subscribe import (
    build_kb_with_channels_to_subscribe,
)
from telegram.src.keyboards.main_menu import build_kb_with_main_menu
from telegram.src.lexicon.ru import LEXICON_RU
from telegram.src.services.subscription_verification import (
    check_subscription_on_channels,
)

logger = getLogger("telegram.handlers.start_conversation")
router: Router = Router()


@router.message(CommandStart())
async def process_start_command(
    msg: Message, config: Config, Session: async_sessionmaker[AsyncSession]
) -> None:
    """Process the /start command."""
    # welcome
    logger.debug("Greet the user.")
    await msg.answer(LEXICON_RU["start"])

    # check subscriptions
    redis_channels_repo = RedisChannelsToSubscribeRepository(
        redis_url=config.redis.url, redis_client=None
    )
    alchemy_channels_repo = SQLAlchemyChannelsToSubscribeRepository(Session)

    logger.debug("Check user subscriptions.")
    await msg.answer(LEXICON_RU["subscription_verification"])
    without_subscription: List[ChannelToSubscribeSchema] = (
        await check_subscription_on_channels(
            user_id=msg.from_user.id,
            bot=msg.bot,
            redis_channels_repo=redis_channels_repo,
            alchemy_channels_repo=alchemy_channels_repo,
        )
    )

    if without_subscription:
        # ask to subscribe
        logger.debug("Ask to subscribe.")
        await msg.answer(
            text=LEXICON_RU["failed_subscription_verification"],
            reply_markup=await build_kb_with_channels_to_subscribe(
                list(without_subscription)
            ),
        )
    else:
        # create if not exists shopping cart
        await create_shopping_cart_if_not_exists(Session, msg.from_user.id)
        # show main menu
        logger.debug("Show main menu.")
        await msg.answer(
            text=LEXICON_RU["successful_subscription_verification"],
            reply_markup=build_kb_with_main_menu(),
        )


@router.message(F.text == LEXICON_RU["back_to_main_menu_bt"])
@router.callback_query(F.data == BACK_TO_MAIN_MENU_CALLBACK)
async def back_to_main_menu(msg: Message | CallbackQuery, state: FSMContext):
    """Show main menu."""
    logger.debug("Show main menu.")
    await state.clear()
    await state.set_state(default_state)
    await msg.bot.send_message(
        chat_id=msg.from_user.id,
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
