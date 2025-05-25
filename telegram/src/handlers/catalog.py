"""The module responsible for the handles, responsible for the catalog."""

from logging import getLogger
from typing import Any, Dict

from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from telegram.src.config.app import Config
from telegram.src.db.repositories.categories import AlchemyCategoryRepository
from telegram.src.keyboards import BACK_TO_MAIN_MENU_CALLBACK, CATEGORY_CB
from telegram.src.keyboards.categories import build_kb_with_categories
from telegram.src.lexicon.ru import LEXICON_RU
from telegram.src.states.catalog import FSMCatalog

logger = getLogger("telegram.handlers.catalog")
router: Router = Router()


@router.callback_query(F.data == BACK_TO_MAIN_MENU_CALLBACK)
@router.callback_query(StateFilter(default_state), F.data == CATEGORY_CB)
# cb format - category:page={page}
@router.callback_query(
    StateFilter(FSMCatalog.choose_category),
    F.data.startswith("category:page="),
)
async def show_categories(
    cb: CallbackQuery,
    state: FSMContext,
    config: Config,
    Session: async_sessionmaker[AsyncSession],
) -> None:
    """Show categories."""
    logger.debug("Show categories")
    categories_repo = AlchemyCategoryRepository(Session)

    if cb.data == CATEGORY_CB or cb.data == BACK_TO_MAIN_MENU_CALLBACK:
        page = 0
        per_page = config.categories_per_page
        count_categories = await categories_repo.length()
        logger.debug("Number categories: %d", count_categories)
        pages = count_categories // per_page
        await state.set_state(FSMCatalog.choose_category)
        await state.update_data(pages=pages, per_page=per_page)
    else:
        page = int(cb.data.split(":")[1].split("=")[1])
        pagination_data: Dict[str, Any] = await state.get_data()
        per_page, pages = pagination_data["per_page"], pagination_data["pages"]

    logger.debug("Number pages: %d", pages)
    logger.debug("Current page: %d", page)
    logger.debug("Per page: %d", per_page)

    await cb.message.edit_text(
        text=LEXICON_RU["catalog"],
        reply_markup=await build_kb_with_categories(
            categories_repo, page, pages, per_page
        ),
    )
