"""The module responsible for Product requests."""

from typing import Optional, Sequence, Tuple

from sqlalchemy import and_, func, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from telegram.src.db.models import Product, ProductShoppingCart


async def add_product_into_shopping_cart(
    Session: async_sessionmaker[AsyncSession],
    product_id: int,
    user_id: int,
    count: int,
) -> None:
    """Add product into shopping cart."""
    async with Session() as session:
        query = insert(ProductShoppingCart).values(
            product_id=product_id,
            shopping_cart_id=user_id,
            count=count,
        )
        query = query.on_conflict_do_update(
            index_elements=["product_id", "shopping_cart_id"],
            set_={"count": ProductShoppingCart.count + query.excluded.count},
        )
        await session.execute(query)
        await session.commit()


async def get_products_from_shopping_cart(
    Session: async_sessionmaker[AsyncSession],
    user_id: int,
    offset: Optional[int] = None,
    limit: Optional[int] = None,
) -> Sequence[Tuple[Product, int]]:
    """Get all products from shopping cart."""
    async with Session() as session:
        query = (
            select(Product, ProductShoppingCart.count)
            .join_from(
                Product,
                ProductShoppingCart,
                Product.id == ProductShoppingCart.product_id,
            )
            .where(ProductShoppingCart.shopping_cart_id == user_id)
            .order_by(Product.name)
        )
        if offset is not None:
            query = query.offset(offset)
        if limit is not None:
            query = query.limit(limit)

        result = await session.execute(query)
        return result.all()


async def get_count_products_in_shopping_cart(
    Session: async_sessionmaker[AsyncSession], user_id: int
) -> int:
    """Get number of products in shopping cart."""
    async with Session() as session:
        query = (
            select(func.count())
            .select_from(ProductShoppingCart)
            .where(ProductShoppingCart.shopping_cart_id == user_id)
        )
        result = await session.execute(query)
        return result.scalar()


async def remove_product_from_shopping_cart(
    Session: async_sessionmaker[AsyncSession], user_id: int, product_id: int
) -> bool:
    """Remove product from shopping cart."""
    async with Session() as session:
        query = (
            select(ProductShoppingCart).where(
                and_(
                    ProductShoppingCart.product_id == product_id,
                    ProductShoppingCart.shopping_cart_id == user_id,
                )
            )
        ).with_for_update()
        result = await session.execute(query)
        product_shopping_cart: Optional[ProductShoppingCart] = (
            result.scalars().first()
        )
        if not product_shopping_cart:
            return False
        await session.delete(product_shopping_cart)
        await session.commit()
        return True
