"""The module responsible for the handles, responsible for the catalog."""

from logging import getLogger
from typing import Optional

from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from telegram.src.config.app import Config
from telegram.src.db.queries.categories import get_number_children
from telegram.src.keyboards import BACK_TO_MAIN_MENU_CALLBACK, CATEGORY_CB
from telegram.src.keyboards.categories import build_kb_with_categories
from telegram.src.states.catalog import FSMCatalog

logger = getLogger("telegram.handlers.catalog")
router: Router = Router()


@router.callback_query(F.data == BACK_TO_MAIN_MENU_CALLBACK)
@router.callback_query(StateFilter(default_state), F.data == CATEGORY_CB)
async def show_categories(
    cb: CallbackQuery,
    state: FSMContext,
    config: Config,
    Session: async_sessionmaker[AsyncSession],
) -> None:
    """Show categories."""
    logger.debug("Show categories")

    category_id: Optional[int] = None
    path: str = "/"
    page = 0
    per_page = config.categories_per_page
    count_categories = await get_number_children(Session)
    logger.debug("Number categories: %d", count_categories)
    pages = count_categories // per_page
    await state.set_state(FSMCatalog.choose_category)

    await cb.message.edit_text(
        text=path,
        reply_markup=await build_kb_with_categories(
            Session, page, pages, path, per_page, category_id
        ),
    )


@router.callback_query(
    StateFilter(FSMCatalog.choose_category),
    F.data.startswith("category:page="),
)
async def pagination_categories(
    cb: CallbackQuery,
    config: Config,
    Session: async_sessionmaker[AsyncSession],
) -> None:
    """Paginate categories."""
    logger.debug("Show categories")

    data_str: str = cb.data.split(":")[1]
    page_str, category_id_str, path_str = data_str.split(";")
    page = int(page_str.split("=")[1])
    category_id_str = category_id_str.split("=")[1]
    category_id: Optional[int] = (
        None if category_id_str == "" else int(category_id_str)
    )
    path = path_str.split("=")[1]

    per_page = config.categories_per_page
    count_categories = await get_number_children(Session, root_id=category_id)
    logger.debug("Number categories: %d", count_categories)
    pages = count_categories // per_page

    await cb.message.edit_text(
        text=path,
        reply_markup=await build_kb_with_categories(
            Session, page, pages, path, per_page, category_id
        ),
    )
