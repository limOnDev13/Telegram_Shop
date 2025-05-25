from abc import ABC, abstractmethod
from typing import Optional, List

from schemas.categories import CategorySchema


class BaseCategoryRepository(ABC):
    @abstractmethod
    async def add(self, category_schema: CategorySchema) -> None:
        pass

    @abstractmethod
    async def get_by_id(self, category_id: int) -> Optional[CategorySchema]:
        pass

    @abstractmethod
    async def remove(self, category_id: int) -> None:
        pass

    @abstractmethod
    async def update(self, category_id: int, new_category_schema: CategorySchema) -> None:
        pass

    @abstractmethod
    async def get_per_page(self, page: int, per_page: int) -> List[CategorySchema]:
        pass

    @abstractmethod
    async def length(self) -> int:
        pass
