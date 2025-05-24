"""The module responsible for getting the configuration from the env vars."""

import os
from dataclasses import dataclass
from typing import List


@dataclass
class BotConfig(object):
    """Bot config."""

    token: str


@dataclass
class Config(object):
    """Total config."""

    debug: bool
    bot: BotConfig
    channels_to_subscribe: List[str]


def get_config() -> Config:
    """Get config from env vars."""
    return Config(
        debug=os.getenv("DEBUG", "0") == "1",
        bot=BotConfig(
            token=os.getenv("BOT_TOKEN", "Bot token from BotFather"),
        ),
        channels_to_subscribe=os.getenv("CHANNELS_TO_SUBSCRIBE", "").split(
            ","
        ),
    )
