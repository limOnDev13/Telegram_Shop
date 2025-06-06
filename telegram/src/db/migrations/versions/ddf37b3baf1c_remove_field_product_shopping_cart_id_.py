"""Remove field product_shopping_cart_id from shopping_cart

Revision ID: ddf37b3baf1c
Revises: 7529027772b3
Create Date: 2025-05-26 19:01:57.657012

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ddf37b3baf1c'
down_revision: Union[str, None] = '7529027772b3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f('shopping_cart_product_shopping_cart_id_fkey'), 'shopping_cart', type_='foreignkey')
    op.drop_column('shopping_cart', 'product_shopping_cart_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('shopping_cart', sa.Column('product_shopping_cart_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.create_foreign_key(op.f('shopping_cart_product_shopping_cart_id_fkey'), 'shopping_cart', 'product_shopping_cart', ['product_shopping_cart_id'], ['id'])
    # ### end Alembic commands ###
