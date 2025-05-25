"""The module responsible for assembling the keyboard with the categories."""

from logging import getLogger
from typing import List

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from repositories.categories.base import BaseCategoryRepository
from schemas.categories import CategorySchema
from telegram.src.keyboards import (
    BACK_TO_MAIN_MENU_CALLBACK,
    CATEGORY_CUR_PAGE_CALLBACK,
    CATEGORY_PAGINATION,
)
from telegram.src.lexicon.ru import LEXICON_RU

logger = getLogger("telegram.keyboards.categories")


def category_bt(category_schema: CategorySchema) -> InlineKeyboardButton:
    """Create inline button with category."""
    return InlineKeyboardButton(
        text=category_schema.name,
        callback_data=f"category_{category_schema.id}",
    )


async def build_kb_with_categories(
    categories_repo: BaseCategoryRepository,
    page: int,
    pages: int,
    per_page: int = 10,
) -> InlineKeyboardMarkup:
    """Build a keyboard with categories."""
    logger.debug("Create kb with categories buttons.")
    per_page = max(10, per_page)
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

    category_bts: List[InlineKeyboardButton] = [
        category_bt(category_schema)
        for category_schema in await categories_repo.get_per_page(
            page, per_page
        )
    ]
    kb_builder.row(*category_bts, width=1)

    back_bt = InlineKeyboardButton(
        text=LEXICON_RU["back_bt"],
        callback_data=CATEGORY_PAGINATION.format(page=page - 1),
    )
    next_bt = InlineKeyboardButton(
        text=LEXICON_RU["next_bt"],
        callback_data=CATEGORY_PAGINATION.format(page=page + 1),
    )
    cur_page_bt = InlineKeyboardButton(
        text=LEXICON_RU["cur_page_bt"].format(page=page + 1, pages=pages + 1),
        callback_data=CATEGORY_CUR_PAGE_CALLBACK,
    )
    if page <= 0:
        kb_builder.row(*(cur_page_bt, next_bt), width=3)
    elif page >= pages:
        kb_builder.row(*(back_bt, cur_page_bt), width=3)
    elif pages == 0:
        kb_builder.row(cur_page_bt, width=3)
    else:
        kb_builder.row(*(back_bt, cur_page_bt, next_bt), width=3)

    main_menu = InlineKeyboardButton(
        text=LEXICON_RU["back_to_main_menu_bt"],
        callback_data=BACK_TO_MAIN_MENU_CALLBACK,
    )
    kb_builder.row(main_menu, width=1)

    return kb_builder.as_markup(resize_keyboard=True)
