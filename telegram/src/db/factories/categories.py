"""Module with factories."""

import random
from typing import List

import factory

from telegram.src.db.models import Category

from .base import BaseFactory, Session


class CategoryFactory(BaseFactory):
    """Category factory."""

    class Meta:
        """Meta class."""

        model = Category

    name: str = factory.Faker("word")


if __name__ == "__main__":
    count_categories: int = int(input("Number categories: "))
    one_tree: str = input("One tree?(yes/no) ").strip().lower()

    with Session() as session:
        categories: List[Category] = list()
        for i in range(count_categories):
            if i == 0:
                category = CategoryFactory.build(parent=None, parent_id=None)
            else:
                random_parent = random.choice(categories)
                if one_tree == "yes":
                    category = CategoryFactory.build(
                        parent=random_parent, parent_id=random_parent.id
                    )
                else:
                    if random.random() < 0.5:
                        category = CategoryFactory.build(
                            parent=random_parent, parent_id=random_parent.id
                        )
                    else:
                        category = CategoryFactory.build(
                            parent=None, parent_id=None
                        )
            session.add(category)
            session.commit()
            session.refresh(category)
            categories.append(category)
