"""The module responsible for ShoppingCart requests."""

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from telegram.src.db.models.shopping_cart import ShoppingCart


async def create_shopping_cart_if_not_exists(
    Session: async_sessionmaker[AsyncSession], user_id: int
) -> None:
    """Create shopping cart for user (shopping_cart.id = user_id)."""
    async with Session() as session:
        query = (
            insert(ShoppingCart)
            .values(id=user_id)
            .on_conflict_do_nothing(index_elements=("id",))
        )
        await session.execute(query)
        await session.commit()
