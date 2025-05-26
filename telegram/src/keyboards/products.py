"""The module responsible for keyboards for viewing products."""

from aiogram.utils.keyboard import (
    KeyboardButton,
    ReplyKeyboardBuilder,
    ReplyKeyboardMarkup,
)

from telegram.src.lexicon.ru import LEXICON_RU


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
