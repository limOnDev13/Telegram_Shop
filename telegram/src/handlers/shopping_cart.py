"""The module responsible for the handlers for viewing shopping cart."""

from logging import getLogger
from typing import Optional

from aiogram import F, Router
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from telegram.src.config.app import Config
from telegram.src.db.models.product import Product
from telegram.src.db.queries.product_shopping_cart import (
    remove_product_from_shopping_cart,
)
from telegram.src.db.queries.products import get_product_by_id
from telegram.src.keyboards import SHOPPING_CART_CB
from telegram.src.keyboards.shopping_cart import (
    build_kb_to_buy_product_from_cart,
)
from telegram.src.lexicon.ru import LEXICON_RU
from telegram.src.services.products import send_product
from telegram.src.services.shopping_cart import view_shopping_cart

logger = getLogger("telegram.handlers.shopping_cart")
router: Router = Router()


@router.callback_query(F.data == SHOPPING_CART_CB)
async def view_shopping_cart_handler(
    cb: CallbackQuery,
    Session: async_sessionmaker[AsyncSession],
    config: Config,
):
    """View shopping cart."""
    await view_shopping_cart(
        bot=cb.bot, Session=Session, user_id=cb.from_user.id, config=config
    )


# cb data format is shopping_cart|pagination:page={page}
@router.callback_query(F.data.startswith("shopping_cart|pagination:page="))
async def pagination_shopping_cart(
    cb: CallbackQuery,
    Session: async_sessionmaker[AsyncSession],
    config: Config,
):
    """Show the product page in the shopping cart."""
    cb_data: str = cb.data.split(":")[1]
    page: int = int(cb_data.split("=")[1])
    await view_shopping_cart(
        bot=cb.bot,
        Session=Session,
        user_id=cb.from_user.id,
        config=config,
        page=page,
    )


# cb data format is shopping_cart|view_product:product_id={product_id};count={count}
@router.callback_query(
    F.data.startswith("shopping_cart|view_product:product_id=")
)
async def buy_product_from_cart_handler(
    cb: CallbackQuery,
    Session: async_sessionmaker[AsyncSession],
):
    """Show a detailed product page from the shopping cart."""
    cb_data: str = cb.data.split(":")[1]
    product_id_data, count_data = cb_data.split(";")
    # TODO: add count into button tu buy product
    product_id, _ = int(product_id_data.split("=")[1]), int(
        count_data.split("=")[1]
    )
    product: Optional[Product] = await get_product_by_id(Session, product_id)

    if product is None:
        await cb.bot.send_message(
            chat_id=cb.from_user.id, text=LEXICON_RU["product_not_found"]
        )
    else:
        await send_product(
            cb,
            product,
            inline_kb=build_kb_to_buy_product_from_cart(product_id),
        )


# shopping_cart|remove:product_id={product_id}
@router.callback_query(F.data.startswith("shopping_cart|remove:product_id="))
async def remove_product_from_cart_handler(
    cb: CallbackQuery,
    Session: async_sessionmaker[AsyncSession],
    config: Config,
):
    """Remove product from the shopping cart."""
    cb_data: str = cb.data.split(":")[1]
    product_id = int(cb_data.split("=")[1])
    record_was_exist: bool = await remove_product_from_shopping_cart(
        Session, cb.from_user.id, product_id
    )
    if record_was_exist:
        await view_shopping_cart_handler(cb, Session, config)
