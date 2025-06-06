"""Make unique pair name and parent_id

Revision ID: e98e6573ac14
Revises: acd1dadff131
Create Date: 2025-05-25 16:26:29.297478

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e98e6573ac14'
down_revision: Union[str, None] = 'acd1dadff131'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f('category_name_key'), 'category', type_='unique')
    op.create_unique_constraint('unique_children_names', 'category', ['name', 'parent_id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('unique_children_names', 'category', type_='unique')
    op.create_unique_constraint(op.f('category_name_key'), 'category', ['name'], postgresql_nulls_not_distinct=False)
    # ### end Alembic commands ###
