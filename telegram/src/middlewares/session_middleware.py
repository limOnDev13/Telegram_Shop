"""The module responsible for the middleware for forwarding the session fabric."""

from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


class SessionFabricMiddleware(BaseMiddleware):
    """Middleware for forwarding Session fabric inside handlers."""

    def __init__(self, session_fabric: async_sessionmaker[AsyncSession]):
        """
        Init class.

        :param session_fabric: Async Session fabric.
        """
        self.__session_fabric = session_fabric

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        """Forward session fabric object inside handler."""
        data["Session"] = self.__session_fabric
        return await handler(event, data)
