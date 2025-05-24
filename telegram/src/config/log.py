"""The module responsible for logging configuration."""

from copy import deepcopy
from typing import Any, Dict

from .app import Config

LOG_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "base": {
            "format": "[%(levelname)s] [%(asctime)s] "
            "| %(name)s %(funcName)s |  %(message)s"
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "base",
        },
        "file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": "INFO",
            "formatter": "base",
            "filename": "./logs/logfile.log",
            "backupCount": 3,
            "when": "d",
            "interval": 10,
            "encoding": "utf-8",
        },
    },
    "loggers": {
        "total": {
            "level": "DEBUG",
            "handlers": ["file", "console"],
            "propagate": False,
        },
        "telegram": {
            "level": "DEBUG",
            "handlers": ["file", "console"],
            "propagate": False,
        },
    },
}


def get_log_config(config: Config) -> Dict[str, Any]:
    """Get config dict for logging."""
    if not config.debug:
        log_config: Dict[str, Any] = deepcopy(LOG_CONFIG)
        log_config["handlers"]["console"]["level"] = "INFO"
        log_config["loggers"]["total"]["level"] = "INFO"
        log_config["loggers"]["telegram"]["level"] = "INFO"
    else:
        log_config = LOG_CONFIG
    return log_config
