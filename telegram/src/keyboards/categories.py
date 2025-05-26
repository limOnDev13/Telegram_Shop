"""The module responsible for assembling the keyboard with the categories."""

from logging import getLogger
from typing import List, Optional

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

import telegram.src.db.queries.categories as q
from telegram.src.keyboards import (
    BACK_TO_MAIN_MENU_CALLBACK,
    CATEGORY_CUR_PAGE_CALLBACK,
    CATEGORY_PAGINATION,
    PRODUCT_CB,
)
from telegram.src.lexicon.ru import LEXICON_RU

logger = getLogger("telegram.keyboards.categories")


def category_bt(
    text: str,
    category_id: int | str,
    path: str,
    number_subcategories: Optional[int] = None,
    page: int = 0,
) -> InlineKeyboardButton:
    """Create inline button with category."""
    if number_subcategories is not None and number_subcategories == 0:
        cb_data: str = PRODUCT_CB.format(
            category_id=category_id,
        )
    else:
        cb_data = CATEGORY_PAGINATION.format(
            page=page,
            category_id=category_id,
            path=path,
        )
        if len(cb_data) >= 64:
            path = path.split("/")[-1]
            path = f".../{path}"
        cb_data = CATEGORY_PAGINATION.format(
            page=page,
            category_id=category_id,
            path=path,
        )

    return InlineKeyboardButton(
        text=text,
        callback_data=cb_data,
    )


async def build_kb_with_categories(
    session_factory: async_sessionmaker[AsyncSession],
    page: int,
    pages: int,
    path: str,
    per_page: int = 10,
    root_id: Optional[int] = None,
) -> InlineKeyboardMarkup:
    """Build a keyboard with categories."""
    logger.debug("Create kb with categories buttons.")
    per_page = max(10, per_page)
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

    category_bts: List[InlineKeyboardButton] = [
        category_bt(
            text=category.name,
            category_id=category.id,
            page=0,
            number_subcategories=number_children,
            path="/".join((path, category.name)),
        )
        for category, number_children in await q.get_categories_by_root_id(
            session_fabric=session_factory,
            root_id=root_id,
            offset=page * per_page,
            limit=per_page,
        )
    ]
    kb_builder.row(*category_bts, width=1)

    back_bt = category_bt(
        text=LEXICON_RU["back_bt"],
        category_id=root_id if root_id else "",
        path=path,
        page=page - 1,
    )
    next_bt = category_bt(
        text=LEXICON_RU["next_bt"],
        category_id=root_id if root_id else "",
        path=path,
        page=page + 1,
    )
    cur_page_bt = InlineKeyboardButton(
        text=LEXICON_RU["cur_page_bt"].format(page=page + 1, pages=pages + 1),
        callback_data=CATEGORY_CUR_PAGE_CALLBACK,
    )
    if pages == 0:
        kb_builder.row(cur_page_bt, width=3)
    elif page <= 0:
        kb_builder.row(*(cur_page_bt, next_bt), width=3)
    elif page >= pages:
        kb_builder.row(*(back_bt, cur_page_bt), width=3)
    else:
        kb_builder.row(*(back_bt, cur_page_bt, next_bt), width=3)

    main_menu = InlineKeyboardButton(
        text=LEXICON_RU["back_to_main_menu_bt"],
        callback_data=BACK_TO_MAIN_MENU_CALLBACK,
    )
    kb_builder.row(main_menu, width=1)

    return kb_builder.as_markup(resize_keyboard=True)
