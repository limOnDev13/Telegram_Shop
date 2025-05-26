"""The module responsible for queries to the categories table."""

from typing import List, Optional, Tuple

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from telegram.src.db.models.category import Category


async def get_categories_by_root_id(
    session_fabric: async_sessionmaker[AsyncSession],
    root_id: Optional[int] = None,
    offset: Optional[int] = None,
    limit: Optional[int] = None,
) -> List[Tuple[Category, int]]:
    """Get categories by root_id."""
    async with session_fabric() as session:
        id_and_number_children = (
            select(
                Category.parent_id,
                func.count(Category.parent_id).label("number_children"),
            )
            .where(Category.parent_id.is_not(None))
            .group_by(Category.parent_id)
        ).subquery()

        query = (
            select(
                Category,
                func.coalesce(id_and_number_children.c.number_children, 0),
            )
            .outerjoin(
                id_and_number_children,
                Category.id == id_and_number_children.c.parent_id,
            )
            .where(Category.parent_id == root_id)
            .order_by(Category.name)
        )
        if offset:
            query = query.offset(offset)
        if limit:
            query = query.limit(limit)

        subcategories_q = await session.execute(query)
        return list(subcategories_q.all())


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
