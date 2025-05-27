"""The module responsible for the business logic of working with the shopping cart."""

from aiogram import Bot
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from telegram.src.config.app import Config
from telegram.src.db.queries.product_shopping_cart import (
    get_count_products_in_shopping_cart,
)
from telegram.src.keyboards.shopping_cart import build_kb_with_shopping_cart
from telegram.src.lexicon.ru import LEXICON_RU


async def view_shopping_cart(
    bot: Bot,
    Session: async_sessionmaker[AsyncSession],
    user_id: int,
    config: Config,
    page: int = 0,
):
    """View the shopping cart."""
    count_products: int = await get_count_products_in_shopping_cart(
        Session, user_id
    )
    per_page: int = config.products_in_shopping_cart_per_page
    pages = count_products // per_page

    await bot.send_message(
        text=LEXICON_RU["shopping_cart"],
        chat_id=user_id,
        reply_markup=await build_kb_with_shopping_cart(
            Session, user_id, page, per_page, pages
        ),
    )
