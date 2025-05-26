"""Module with product factory."""

import random
from decimal import Decimal
from typing import List

import factory
from sqlalchemy import select

from telegram.src.db.models import Category, Product

from .base import BaseFactory, Session


class ProductFactory(BaseFactory):
    """Product factory."""

    class Meta:
        """Meta class."""

        model = Product

    name: str = factory.Faker("word")
    img_path: str = "./media/test.jpeg"
    description: str = factory.Faker("text", max_nb_chars=4000)
    price: Decimal = factory.LazyAttribute(
        lambda _: round(random.uniform(0, 100), 2)
    )


if __name__ == "__main__":
    count_products: int = int(input("Number products for each subcategory: "))

    with Session() as session:
        # Получим id всех категорий, которые являются родительскими узлами
        subquery = (
            select(Category.parent_id)
            .where(Category.parent_id.is_not(None))
            .distinct()
        )

        # Получим id категорий, которые являются листьями
        # (не являются родительскими узлами)
        query = select(Category.id).where(Category.id.not_in(subquery))
        result = session.scalars(query)
        category_ids: List[int] = result.all()

        products: List[Product] = [
            ProductFactory.build(category_id=random.choice(category_ids))
            for _ in range(count_products)
        ]
        session.add_all(products)
        session.commit()
