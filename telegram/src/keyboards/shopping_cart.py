"""The module responsible for keyboards for viewing products."""

from logging import getLogger
from typing import List

from aiogram.utils.keyboard import (
    InlineKeyboardBuilder,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from telegram.src.db.models import Product
from telegram.src.db.queries.product_shopping_cart import (
    get_products_from_shopping_cart,
)
from telegram.src.keyboards import (
    BACK_TO_MAIN_MENU_CALLBACK,
    BUY_PRODUCT_CB,
    SHOPPING_CART_BUY_PRODUCT_CB,
    SHOPPING_CART_CUR_PAGE_CB,
    SHOPPING_CART_MAKING_ORDER,
    SHOPPING_CART_PAGINATION_CB,
    SHOPPING_CART_REMOVE_PRODUCT_CB,
)
from telegram.src.lexicon.ru import LEXICON_RU

logger = getLogger("telegram.keyboards.products")


def build_kb_for_buying_product(product: Product) -> InlineKeyboardMarkup:
    """Build a keyboard with categories."""
    logger.debug("Create kb for buying the product.")
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    buy_button = InlineKeyboardButton(
        text=LEXICON_RU["buy_button"].format(
            name=product.name,
            price=product.price,
        ),
        callback_data=BUY_PRODUCT_CB.format(product_id=product.id),
    )
    kb_builder.row(buy_button, width=1)

    return kb_builder.as_markup(resize_keyboard=True)


def product_in_sc_bt(
    product: Product, num_products: int
) -> InlineKeyboardButton:
    """Create button with product in shopping cart."""
    return InlineKeyboardButton(
        text=LEXICON_RU["product_in_sc"].format(
            name=product.name,
            price=product.price,
            count=num_products,
            total=product.price * num_products,
        ),
        callback_data=SHOPPING_CART_BUY_PRODUCT_CB.format(
            product_id=product.id,
            count=num_products,
        ),
    )


async def build_kb_with_shopping_cart(
    Session: async_sessionmaker[AsyncSession],
    user_id: int,
    page: int,
    per_page: int,
    pages: int,
) -> InlineKeyboardMarkup:
    """Build a keyboard with shopping cart."""
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

    products_bts: List[InlineKeyboardButton] = [
        product_in_sc_bt(product, count)
        for product, count in await get_products_from_shopping_cart(
            Session=Session,
            user_id=user_id,
            offset=page * per_page,
            limit=per_page,
        )
    ]
    kb_builder.row(*products_bts, width=1)

    back_bt = InlineKeyboardButton(
        text=LEXICON_RU["back_bt"],
        callback_data=SHOPPING_CART_PAGINATION_CB.format(page=page - 1),
    )
    next_bt = InlineKeyboardButton(
        text=LEXICON_RU["next_bt"],
        callback_data=SHOPPING_CART_PAGINATION_CB.format(page=page + 1),
    )
    cur_page_bt = InlineKeyboardButton(
        text=LEXICON_RU["cur_page_bt"].format(page=page + 1, pages=pages + 1),
        callback_data=SHOPPING_CART_CUR_PAGE_CB,
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


def build_kb_to_buy_product_from_cart(
    product_id: int, count: int
) -> InlineKeyboardMarkup:
    """Create kb for viewing the product from shopping cart."""
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

    buy_bt = InlineKeyboardButton(
        text=LEXICON_RU["buy_product_bt"],
        # shopping_cart|order:product_id={product_id};count={count}
        callback_data=SHOPPING_CART_MAKING_ORDER.format(
            product_id=product_id,
            count=count,
        ),
    )
    remove_bt = InlineKeyboardButton(
        text=LEXICON_RU["remove_from_cart"],
        callback_data=SHOPPING_CART_REMOVE_PRODUCT_CB.format(
            product_id=product_id
        ),
    )
    kb_builder.row(buy_bt, remove_bt, width=2)
    return kb_builder.as_markup(resize_keyboard=True)
