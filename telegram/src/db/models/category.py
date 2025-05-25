"""The module responsible for the category model."""

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Category(Base):
    """Category model."""

    __tablename__ = "category"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    name: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
