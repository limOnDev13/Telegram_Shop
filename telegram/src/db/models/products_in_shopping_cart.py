"""The module responsible for the product_shopping_cart model."""

from sqlalchemy import (
    ForeignKey,
    Integer,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class ProductShoppingCart(Base):
    """ProductShoppingCart model."""

    __tablename__ = "product_shopping_cart"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    product_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("product.id"), nullable=False
    )
    shopping_cart_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("shopping_cart.id"), nullable=False
    )
    count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    product: Mapped["Product"] = relationship(
        "Product",
        single_parent=True,
    )
    shopping_cart: Mapped["ShoppingCart"] = relationship(
        "ShoppingCart",
        single_parent=True,
        back_populates="products",
    )

    __table_args__ = (
        UniqueConstraint(
            "product_id",
            "shopping_cart_id",
            name="unique_pair_product_and_shopping_cart",
        ),
    )
