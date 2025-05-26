"""The module responsible for queries to the product table."""

from typing import Optional, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from telegram.src.db.models.product import Product


async def get_products_with_category_id(
    Session: async_sessionmaker[AsyncSession],
    category_id: int,
    offset: Optional[int] = None,
    limit: Optional[int] = None,
) -> Sequence[Product]:
    """Get products by category_id."""
    async with Session() as session:
        query = (
            select(Product)
            .where(Product.category_id == category_id)
            .order_by(Product.name)
        )
        if offset is not None:
            query = query.offset(offset)
        if limit is not None:
            query = query.limit(limit)

        results = await session.execute(query)
        return results.scalars().all()
