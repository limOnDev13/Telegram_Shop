"""The module responsible for getting the configuration from the env vars."""

import os
from dataclasses import dataclass
from typing import List


@dataclass
class BotConfig(object):
    """Bot config."""

    token: str


@dataclass
class PostgresConfig(object):
    """Postgres Config."""

    url: str
    sync_url: str


@dataclass
class RedisConfig(object):
    """Redis config."""

    url: str


@dataclass
class Config(object):
    """Total config."""

    debug: bool
    categories_per_page: int
    bot: BotConfig
    redis: RedisConfig
    postgres: PostgresConfig


def get_config() -> Config:
    """Get config from env vars."""
    debug: bool = os.getenv("DEBUG", "0") == "1"
    return Config(
        debug=debug,
        categories_per_page=int(os.getenv("CATEGORIES_PER_PAGE", 10)),
        bot=BotConfig(
            token=os.getenv("BOT_TOKEN", "Bot token from BotFather"),
        ),
        redis=RedisConfig(
            url=(
                os.getenv("REDIS_TEST_URL", "Redis test url")
                if debug
                else os.getenv("REDIS_URL", "Redis url")
            ),
        ),
        postgres=PostgresConfig(
            url=(
                os.getenv("POSTGRES_TEST_URL", "Postgres test url")
                if debug
                else os.getenv("POSTGRES_URL", "Postgres prod url")
            ),
            sync_url=(
                os.getenv("POSTGRES_TEST_SYNC_URL", "Postgres test sync url")
                if debug
                else os.getenv("POSTGRES_SYNC_URL", "Postgres sync url")
            ),
        ),
    )
