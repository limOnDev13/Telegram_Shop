"""The module responsible for assembling the keyboard with the main menu."""
from logging import getLogger

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from telegram.src.lexicon.ru import LEXICON_RU

logger = getLogger("telegram.keyboards.main_menu")


def build_kb_with_main_menu() -> InlineKeyboardMarkup:
    """Build a keyboard with main menu."""
    logger.debug("Create kb with main menu buttons.")
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

    catalog_bt: InlineKeyboardButton = InlineKeyboardButton(
        text=LEXICON_RU["catalog_bt"]
    )
    shopping_cart_bt: InlineKeyboardButton = InlineKeyboardButton(
        text=LEXICON_RU["shopping_cart_bt"]
    )
    faq_bt: InlineKeyboardButton = InlineKeyboardButton(
        text=LEXICON_RU["faq_bt"]
    )

    kb_builder.row(*(catalog_bt, shopping_cart_bt, faq_bt), width=3)

    return kb_builder.as_markup(resize_keyboard=True)
