"""Delete field refresh_token in table User

Revision ID: 84f9486ed355
Revises: f16ca3183da9
Create Date: 2024-11-04 13:36:25.325337

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '84f9486ed355'
down_revision: Union[str, None] = 'f16ca3183da9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'refresh_token')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('refresh_token', sa.VARCHAR(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
