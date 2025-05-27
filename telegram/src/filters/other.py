"""Modules responsible for various filters."""

from aiogram.filters import BaseFilter
from aiogram.types import Message


class InputIsPositiveNumber(BaseFilter):
    """Filter for positive integers."""

    async def __call__(self, message: Message) -> bool:
        """Check input."""
        input_str: str = message.text.strip()

        return input_str.isdigit() and int(input_str) > 0
