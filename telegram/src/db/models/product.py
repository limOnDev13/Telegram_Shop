"""The module responsible for the product model."""

from decimal import Decimal
from typing import Optional

from sqlalchemy import (
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Product(Base):
    """Product model."""

    __tablename__ = "product"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    name: Mapped[str] = mapped_column(String(20), nullable=False)
    img_path: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    price: Mapped[Decimal] = mapped_column(
        Numeric(precision=10, scale=2), nullable=False
    )
    category_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("category.id"), nullable=False
    )
    category: Mapped["Category"] = relationship(
        "Category",
        single_parent=True,
        back_populates="products",
        foreign_keys=[category_id],
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        UniqueConstraint(
            "name", "category_id", name="unique_pair_name_and_category_id"
        ),
    )
