"""Module with factories."""

import factory

from telegram.src.db.models import Category

from .base import BaseFactory


class CategoryFactory(BaseFactory):
    """Category factory."""

    class Meta:
        """Meta class."""

        model = Category

    name: str = factory.Faker("word")


if __name__ == "__main__":
    count_categories: int = int(input("Number categories: "))

    CategoryFactory.create_batch(size=count_categories)
