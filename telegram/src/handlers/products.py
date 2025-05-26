"""The module responsible for the handlers for viewing products."""

from logging import getLogger
from typing import Any, Dict

from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from telegram.src.config.app import Config
from telegram.src.lexicon.ru import LEXICON_RU
from telegram.src.services.products import send_some_products
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
    msg: CallbackQuery | Message,
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
