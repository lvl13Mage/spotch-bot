"""Update Spotify Token, Drop old Databases

Revision ID: 54c8a91300bd
Revises: 
Create Date: 2025-04-06 13:21:18.729929

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '54c8a91300bd'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('spotify_token', schema=None) as batch_op:
        batch_op.alter_column('expires_in',
               existing_type=sa.DATETIME(),
               type_=sa.String(),
               existing_nullable=False)
        batch_op.alter_column('expires_at',
               existing_type=sa.DATETIME(),
               type_=sa.String(),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('spotify_token', schema=None) as batch_op:
        batch_op.alter_column('expires_at',
               existing_type=sa.String(),
               type_=sa.DATETIME(),
               existing_nullable=False)
        batch_op.alter_column('expires_in',
               existing_type=sa.String(),
               type_=sa.DATETIME(),
               existing_nullable=False)

    # ### end Alembic commands ###
