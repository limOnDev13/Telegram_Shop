"""The module responsible for assembling the keyboard with the categories."""

from logging import getLogger
from typing import List

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from telegram.src.lexicon.ru import LEXICON_RU
from telegram.src.keyboards import CATEGORY_PAGINATION_CALLBACK, CATEGORY_CUR_PAGE_CALLBACK, BACK_TO_MAIN_MENU_CALLBACK
from repositories.categories.base import BaseCategoryRepository
from schemas.categories import CategorySchema

logger = getLogger("telegram.keyboards.categories")


def category_bt(category_schema: CategorySchema) -> InlineKeyboardButton:
    return InlineKeyboardButton(
        text=category_schema.name,
        callback_data=f"category_{category_schema.id}"
    )

def pagination_bt(text: str, page: int, per_page: int, pages: int) -> InlineKeyboardButton:
    return InlineKeyboardButton(
        text=text,
        callback_data=CATEGORY_PAGINATION_CALLBACK.format(
            page=page,
            per_page=per_page,
            pages=pages
        )
    )


async def build_kb_with_categories(
        categories_repo: BaseCategoryRepository,
        page: int,
        pages: int,
        per_page: int = 10
) -> InlineKeyboardMarkup:
    """Build a keyboard with categories."""
    logger.debug("Create kb with categories buttons.")
    per_page = max(10, per_page)
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

    category_bts: List[InlineKeyboardButton] = [
        category_bt(category_schema)
        for category_schema in await categories_repo.get_per_page(page, per_page)
    ]
    kb_builder.row(*category_bts, width=1)

    back_bt = pagination_bt(LEXICON_RU["back_bt"], 0 if page == 0 else page - 1, per_page, pages)
    next_bt = pagination_bt(LEXICON_RU["next_bt"], pages if page == pages else page + 1, per_page, pages)
    cur_page_bt = InlineKeyboardButton(
        text=LEXICON_RU["cur_page_bt"].format(page=page + 1, pages=pages + 1),
        callback_data=CATEGORY_CUR_PAGE_CALLBACK,
    )
    kb_builder.row(*(back_bt, cur_page_bt, next_bt), width=3)

    main_menu = InlineKeyboardButton(
        text=LEXICON_RU["back_to_main_menu_bt"],
        callback_data=BACK_TO_MAIN_MENU_CALLBACK,
    )
    kb_builder.row(main_menu, width=1)

    return kb_builder.as_markup(resize_keyboard=True)
