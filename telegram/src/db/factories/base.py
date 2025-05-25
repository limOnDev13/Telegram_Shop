"""The module responsible for the basic model factory."""

from dotenv import load_dotenv
from factory.alchemy import SQLAlchemyModelFactory

from telegram.src.config.app import Config, get_config
from telegram.src.db.database import create_sync_session_fabric

load_dotenv()
config: Config = get_config()

Session = create_sync_session_fabric(config)


class BaseFactory(SQLAlchemyModelFactory):
    """Base factory."""

    class Meta:
        """Meta class."""

        abstract = True
        sqlalchemy_session_persistence = "commit"
        sqlalchemy_session_factory = Session
