"""Create solve_requests table

Revision ID: 33f410cd46cb
Revises: a4bf593de022
Create Date: 2024-05-28 20:57:38.847212

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '33f410cd46cb'
down_revision: Union[str, None] = 'a4bf593de022'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###