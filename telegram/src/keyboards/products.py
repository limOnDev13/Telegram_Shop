"""The module responsible for keyboards for viewing products."""

from logging import getLogger

from aiogram.utils.keyboard import (
    InlineKeyboardBuilder,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardBuilder,
    ReplyKeyboardMarkup,
)

from telegram.src.db.models import Product
from telegram.src.keyboards import BUY_PRODUCT_CB
from telegram.src.lexicon.ru import LEXICON_RU

logger = getLogger("telegram.keyboards.products")


def build_kb_for_viewing_products() -> ReplyKeyboardMarkup:
    """Build kb for viewing products."""
    kb_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()

    next_batch_bt: KeyboardButton = KeyboardButton(
        text=LEXICON_RU["next_batch_bt"]
    )
    back_to_main_menu_bt: KeyboardButton = KeyboardButton(
        text=LEXICON_RU["back_to_main_menu_bt"]
    )

    kb_builder.row(*(next_batch_bt, back_to_main_menu_bt), width=2)
    return kb_builder.as_markup(resize_keyboard=True)


def build_kb_for_buying_product(product: Product) -> InlineKeyboardMarkup:
    """Build a keyboard with categories."""
    logger.debug("Create kb for buying the product.")
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    cb_data: str = BUY_PRODUCT_CB.format(product_id=product.id)
    logger.debug("cb data: %s", cb_data)
    buy_button = InlineKeyboardButton(
        text=LEXICON_RU["buy_button"].format(
            name=product.name,
            price=product.price,
        ),
        callback_data=BUY_PRODUCT_CB.format(product_id=product.id),
    )
    kb_builder.row(buy_button, width=1)

    return kb_builder.as_markup(resize_keyboard=True)
