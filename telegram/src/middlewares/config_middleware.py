"""The module responsible for the middleware for forwarding the config."""

from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message

from telegram.src.config.app import Config


class ConfigMiddleware(BaseMiddleware):
    """Middleware for forwarding Config inside handlers."""

    def __init__(self, config: Config):
        """
        Init class.

        :param config: Config object.
        """
        self.__config = config

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        """Forward Config object inside handler."""
        data["config"] = self.__config
        return await handler(event, data)
