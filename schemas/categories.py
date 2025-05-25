"""The module responsible for the category schema."""

from typing import Optional

from pydantic import BaseModel, Field


class CategorySchema(BaseModel):
    """Category schema."""

    id: int = Field(..., description="Category ID.")
    name: str = Field(..., description="Category name.")
    parent_id: Optional[int] = Field(default=None, description="")

    class Config:
        """Config class."""

        from_attributes = True
