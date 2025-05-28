"""The module responsible for the subscription channel model."""

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class ChannelToSubscribe(Base):
    """Channel model."""

    __tablename__ = "channel_to_subscribe"

    id: Mapped[str] = mapped_column(String(20), primary_key=True)
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    url: Mapped[str] = mapped_column(String(), nullable=False)
