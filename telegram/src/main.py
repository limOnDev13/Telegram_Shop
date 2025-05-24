"""The module responsible for launching the bot."""

import asyncio
import logging
import logging.config
from typing import Any, Dict

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    async_sessionmaker,
    create_async_engine,
)

from .config.app import Config, get_config
from .config.log import get_log_config
from .handlers import start_conversation_router
from .middlewares import ConfigMiddleware, SessionFabricMiddleware


async def main():
    """Config and launch bot."""
    # config
    load_dotenv()
    config: Config = get_config()

    # logging
    log_config: Dict[str, Any] = get_log_config(config)
    logging.config.dictConfig(log_config)
    logger = logging.getLogger("telegram")

    # database
    engine: AsyncEngine = create_async_engine(
        config.postgres.url,
        pool_pre_ping=True,
        pool_size=100,
        max_overflow=20,
        pool_timeout=60,
    )
    Session = async_sessionmaker(bind=engine, expire_on_commit=False)

    try:
        # bot
        bot: Bot = Bot(
            token=config.bot.token,
            default=DefaultBotProperties(parse_mode="HTML"),
        )

        # dispatcher
        dp: Dispatcher = Dispatcher()

        # init middlewares
        confid_middleware = ConfigMiddleware(config)
        session_fabric_middleware = SessionFabricMiddleware(Session)

        # register routers
        dp.include_router(start_conversation_router)

        # register middlewares
        start_conversation_router.message.middleware(confid_middleware)
        start_conversation_router.message.middleware(session_fabric_middleware)

        # launch bot
        await bot.delete_webhook(drop_pending_updates=True)
        logger.info("Start bot.")
        await dp.start_polling(bot)
    except Exception as exc:
        logger.critical(str(exc))


if __name__ == "__main__":
    asyncio.run(main())
