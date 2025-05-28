"""The module responsible for the shopping cart model."""

from typing import List

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class ShoppingCart(Base):
    """Shopping cart model."""

    __tablename__ = "shopping_cart"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)  # id = user_id
    products: Mapped[List["ProductShoppingCart"]] = relationship(
        "ProductShoppingCart",
        back_populates="shopping_cart",
    )
