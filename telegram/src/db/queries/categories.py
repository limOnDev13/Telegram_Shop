"""The module responsible for queries to the categories table."""

from typing import List, Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from telegram.src.db.models.category import Category


async def get_categories_by_root_id(
    session_fabric: async_sessionmaker[AsyncSession],
    root_id: Optional[int] = None,
    offset: Optional[int] = None,
    limit: Optional[int] = None,
) -> List[Category]:
    """Get categories by root_id."""
    async with session_fabric() as session:
        query = (
            select(Category)
            .where(Category.parent_id == root_id)
            .order_by(Category.name)
        )
        if offset:
            query = query.offset(offset)
        if limit:
            query = query.limit(limit)

        subcategories_q = await session.execute(query)
        return list(subcategories_q.scalars().all())


async def get_number_children(
    session_fabric: async_sessionmaker[AsyncSession],
    root_id: Optional[int] = None,
) -> int:
    """Get number subcategories."""
    async with session_fabric() as session:
        result = await session.execute(
            select(func.count())
            .select_from(Category)
            .where(Category.parent_id == root_id)
        )
        return result.scalar()
