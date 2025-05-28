"""The module responsible for the sqlalchemy-based repository."""

from typing import List, Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from repositories.categories.base import BaseCategoryRepository
from schemas.categories import CategorySchema
from telegram.src.db.models.category import Category


class AlchemyCategoryRepository(BaseCategoryRepository):
    """SQLAlchemy categories repository."""

    def __init__(self, session_fabric: async_sessionmaker[AsyncSession]):
        """
        Init class.

        :param session_fabric: async session fabric.
        """
        self.__session_fabric = session_fabric

    async def add(self, category_schema: CategorySchema) -> None:
        """Add new category."""
        async with self.__session_fabric() as session:
            category_model = Category(**category_schema.model_dump())
            session.add(category_model)
            await session.commit()

    async def get_by_id(self, category_id: int) -> Optional[CategorySchema]:
        """Get category by id."""
        async with self.__session_fabric() as session:
            return await session.get(Category, category_id)

    async def remove(self, category_id: int) -> None:
        """Remove category."""
        async with self.__session_fabric() as session:
            delete_q = await session.execute(
                select(Category)
                .where(Category.id == category_id)
                .with_for_update()
            )
            category: Optional[Category] = delete_q.first()
            if category:
                await session.delete(category)
                await session.commit()

    async def update(
        self, category_id: int, new_category_schema: CategorySchema
    ) -> None:
        """Update category."""
        async with self.__session_fabric() as session:
            category_q = await session.execute(
                select(Category)
                .where(Category.id == new_category_schema.id)
                .with_for_update()
            )
            category: Optional[Category] = category_q.first()
            if category:
                updated_category = Category(**new_category_schema.model_dump())
                await session.merge(updated_category)
                await session.commit()

    async def get_per_page(
        self, page: int, per_page: int
    ) -> List[CategorySchema]:
        """Get page with categories."""
        async with self.__session_fabric() as session:
            categories_q = await session.execute(
                select(Category)
                .order_by(Category.name)
                .offset(page * per_page)
                .limit(per_page)
            )
            return [
                CategorySchema.model_validate(category)
                for category in categories_q.scalars().all()
            ]
