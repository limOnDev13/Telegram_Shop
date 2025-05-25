"""The module responsible for the category schema."""

from pydantic import BaseModel, Field


class CategorySchema(BaseModel):
    """Category schema."""

    id: int = Field(..., description="Category ID.")
    name: str = Field(..., description="Category name.")

    class Config:
        """Config class."""

        from_attributes = True
