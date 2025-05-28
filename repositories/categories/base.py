"""The module responsible for the basic repositories for categories."""

from abc import ABC, abstractmethod
from typing import List, Optional

from schemas.categories import CategorySchema


class BaseCategoryRepository(ABC):
    """Base category repository."""

    @abstractmethod
    async def add(self, category_schema: CategorySchema) -> None:
        """Add new category."""
        pass

    @abstractmethod
    async def get_by_id(self, category_id: int) -> Optional[CategorySchema]:
        """Get category by id."""
        pass

    @abstractmethod
    async def remove(self, category_id: int) -> None:
        """Remove category."""
        pass

    @abstractmethod
    async def update(
        self, category_id: int, new_category_schema: CategorySchema
    ) -> None:
        """Update category."""
        pass

    @abstractmethod
    async def get_per_page(
        self, page: int, per_page: int
    ) -> List[CategorySchema]:
        """Get page with categories."""
        pass
