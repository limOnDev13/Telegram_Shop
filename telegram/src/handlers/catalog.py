"""The module responsible for the handles, responsible for the catalog."""

from logging import getLogger
import re

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from telegram.src.db.repositories.categories import AlchemyCategoryRepository
from telegram.src.lexicon.ru import LEXICON_RU
from telegram.src.states.catalog import FSMCatalog
from telegram.src.keyboards.categories import build_kb_with_categories

logger = getLogger("telegram.handlers.catalog")
router: Router = Router()


@router.callback_query(
    StateFilter(default_state), F.data == "catalog_bt"
)
async def show_categories(
    cb: CallbackQuery,
    state: FSMContext,
    Session: async_sessionmaker[AsyncSession],
) -> None:
    """Processing of clicking on the "catalog" button."""
    logger.debug("Show categories")
    await state.set_state(FSMCatalog.choose_category)

    categories_repo = AlchemyCategoryRepository(Session)
    per_page: int = 10
    count_categories: int = await categories_repo.length()
    logger.debug("Number categories: %d", count_categories)
    pages: int = (count_categories // per_page) - 1
    logger.debug("Number pages: %d", pages)

    await cb.message.edit_text(
        text=LEXICON_RU["catalog"],
        reply_markup=await build_kb_with_categories(categories_repo, 0, pages, per_page),
    )
