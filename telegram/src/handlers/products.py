"""The module responsible for the handlers for viewing products."""

from logging import getLogger
from typing import Any, Dict

from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from telegram.src.config.app import Config
from telegram.src.db.queries.product_shopping_cart import (
    add_product_into_shopping_cart,
)
from telegram.src.filters.other import InputIsPositiveNumber
from telegram.src.lexicon.ru import LEXICON_RU
from telegram.src.services.products import send_some_products
from telegram.src.services.shopping_cart import view_shopping_cart
from telegram.src.states.catalog import FSMCatalog

logger = getLogger("telegram.handlers.catalog")
router: Router = Router()


# cb_data - product:category_id={category_id}
@router.callback_query(
    StateFilter(FSMCatalog.choose_category),
    F.data.startswith("product:category_id="),
)
async def show_products(
    cb: CallbackQuery,
    state: FSMContext,
    config: Config,
    Session: async_sessionmaker[AsyncSession],
) -> None:
    """Show products."""
    logger.debug("Show products")

    cb_data: str = cb.data.split(":")[1]
    category_id = int(cb_data.split(";")[0].split("=")[1])
    page: int = 0
    await state.set_state(FSMCatalog.view_products)

    await send_some_products(
        cb=cb,
        Session=Session,
        category_id=category_id,
        page=page,
        per_page=config.products_per_page,
    )

    await state.update_data(
        products_page=page + 1, products_category_id=category_id
    )


@router.message(
    StateFilter(FSMCatalog.view_products),
    F.text == LEXICON_RU["next_batch_bt"],
)
async def show_more_products(
    msg: Message,
    state: FSMContext,
    config: Config,
    Session: async_sessionmaker[AsyncSession],
) -> None:
    """Show more products."""
    logger.debug("Show more products")

    state_data: Dict[str, Any] = await state.get_data()
    category_id, page = (
        state_data["products_category_id"],
        state_data["products_page"],
    )

    await send_some_products(
        cb=msg,
        Session=Session,
        category_id=category_id,
        page=page,
        per_page=config.products_per_page,
    )

    await state.update_data(
        products_page=page + 1, products_category_id=category_id
    )


# cb format is product|buy:product_id={product_id}
@router.callback_query(
    StateFilter(FSMCatalog.view_products),
    F.data.startswith("product|buy:product_id="),
)
async def number_of_products_purchased(
    cb: CallbackQuery,
    state: FSMContext,
) -> None:
    """Process the selection of a product to add to the cart."""
    logger.debug("Ask user to input count products")
    await state.set_state(FSMCatalog.input_count_products)

    cb_data = cb.data.split(":")[1]
    product_id: int = int(cb_data.split("=")[1])
    await state.update_data(buy_product_id=product_id)

    await cb.bot.send_message(
        chat_id=cb.from_user.id, text=LEXICON_RU["how_many_products"]
    )


@router.message(
    StateFilter(FSMCatalog.input_count_products),
    InputIsPositiveNumber(),
)
async def correct_input_count_products(
    msg: Message,
    state: FSMContext,
    Session: async_sessionmaker[AsyncSession],
    config: Config,
) -> None:
    """Process the correct input of the number of products."""
    logger.debug("User input correct count of products.")
    state_data = await state.get_data()
    product_id: int = state_data["buy_product_id"]
    await add_product_into_shopping_cart(
        Session=Session,
        product_id=product_id,
        user_id=msg.from_user.id,
        count=int(msg.text),
    )
    await state.set_state(default_state)
    await state.clear()
    await view_shopping_cart(
        bot=msg.bot,
        Session=Session,
        user_id=msg.from_user.id,
        config=config,
    )


@router.message(StateFilter(FSMCatalog.input_count_products))
async def wrong_input_number_products(
    msg: Message,
) -> None:
    """Process the incorrect input of the number of products."""
    await msg.answer(text=LEXICON_RU["wrong_input_while_buying_product"])
