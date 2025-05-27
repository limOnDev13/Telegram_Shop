"""The module responsible for the business logic related to the products."""

from logging import getLogger
from typing import Optional, Sequence

from aiogram.exceptions import TelegramAPIError
from aiogram.types import CallbackQuery, FSInputFile, Message
from aiogram.utils.keyboard import InlineKeyboardMarkup
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from telegram.src.db.models.product import Product
from telegram.src.db.queries.products import get_products_with_category_id
from telegram.src.keyboards.products import (
    build_kb_for_buying_product,
    build_kb_for_viewing_products,
)
from telegram.src.lexicon.ru import LEXICON_RU

logger = getLogger("telegram.services.products")


async def send_some_products(
    cb: CallbackQuery | Message,
    Session: async_sessionmaker[AsyncSession],
    category_id: int,
    page: int,
    per_page: int,
) -> None:
    """Send a photo and description of each product."""
    products: Sequence[Product] = await get_products_with_category_id(
        Session=Session,
        category_id=category_id,
        offset=page * per_page,
        limit=per_page,
    )

    for product in products:
        await send_product(cb, product)


async def send_product(
    cb: CallbackQuery | Message,
    product: Product,
    inline_kb: Optional[InlineKeyboardMarkup] = None,
) -> None:
    """Send a photo and description of the product."""
    try:
        await cb.bot.send_photo(
            chat_id=cb.from_user.id,
            photo=FSInputFile(product.img_path),
            reply_markup=build_kb_for_viewing_products(),
        )
        await cb.bot.send_message(
            chat_id=cb.from_user.id,
            text=LEXICON_RU["product"].format(
                name=product.name,
                description=product.description,
            ),
            reply_markup=(
                build_kb_for_buying_product(product)
                if inline_kb is None
                else inline_kb
            ),
        )
    except FileNotFoundError as exc:
        logger.warning("Img %s not found. %s", product.img_path, str(exc))
    except TelegramAPIError as exc:
        logger.error(
            "Error when sending a file via the telegram API. %s", str(exc)
        )
