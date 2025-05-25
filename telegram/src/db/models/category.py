"""The module responsible for the category model."""

from typing import List, Optional

from sqlalchemy import ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Category(Base):
    """Category model."""

    __tablename__ = "category"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    name: Mapped[str] = mapped_column(String(20), nullable=False)
    parent_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("category.id"),
        nullable=True,
    )
    parent: Mapped[Optional["Category"]] = relationship(
        "Category",
        foreign_keys=[parent_id],
        back_populates="subcategories",
        remote_side=[id],
    )

    subcategories: Mapped[List["Category"]] = relationship(
        "Category",
        back_populates="parent",
        cascade="all, delete-orphan",
    )
    __table_args__ = (
        UniqueConstraint("name", "parent_id", name="unique_children_names"),
    )
