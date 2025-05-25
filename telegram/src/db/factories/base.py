from factory.alchemy import SQLAlchemyModelFactory
from dotenv import load_dotenv

from telegram.src.config.app import get_config, Config
from telegram.src.db.database import create_sync_session_fabric

load_dotenv()
config: Config = get_config()

Session = create_sync_session_fabric(config)


class AsyncBaseFactory(SQLAlchemyModelFactory):
    class Meta:
        abstract = True
        sqlalchemy_session_persistence = "commit"
        sqlalchemy_session_factory = lambda: Session()
