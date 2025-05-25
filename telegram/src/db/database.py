"""The module responsible for connecting to the database."""

from typing import Optional

from sqlalchemy import Engine, create_engine
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import Session, sessionmaker

from telegram.src.config.app import Config


# Async
def create_asyncengine(config: Config) -> AsyncEngine:
    """Get async engine."""
    return create_async_engine(
        config.postgres.url,
        pool_pre_ping=True,
        pool_size=100,
        max_overflow=20,
        pool_timeout=60,
    )


def create_async_session_fabric(
    config: Config, engine: Optional[AsyncEngine] = None
) -> async_sessionmaker[AsyncSession]:
    """Get async session fabric."""
    if engine:
        return async_sessionmaker(bind=engine, expire_on_commit=False)
    return async_sessionmaker(
        bind=create_asyncengine(config), expire_on_commit=False
    )


# Sync
def create_syncengine(config: Config) -> Engine:
    """Get sync engine."""
    return create_engine(
        config.postgres.sync_url,
        pool_pre_ping=True,
        pool_size=100,
        max_overflow=20,
        pool_timeout=60,
    )


def create_sync_session_fabric(
    config: Config, engine: Optional[Engine] = None
) -> sessionmaker[Session]:
    """Get sync session."""
    if engine:
        return sessionmaker(bind=engine, expire_on_commit=False)
    return sessionmaker(bind=create_syncengine(config), expire_on_commit=False)
