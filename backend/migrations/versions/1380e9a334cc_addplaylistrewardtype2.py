"""AddPlaylistRewardType2

Revision ID: 1380e9a334cc
Revises: 54c8a91300bd
Create Date: 2025-04-06 13:41:20.812794

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from backend.modules.twitch.schemas.reward_type import RewardType


# revision identifiers, used by Alembic.
revision: str = '1380e9a334cc'
down_revision: Union[str, None] = '54c8a91300bd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Build the new CHECK constraint
    allowed_values = ", ".join(f"'{t.value}'" for t in RewardType)
    check_constraint = sa.CheckConstraint(f"type IN ({allowed_values})", name="reward_type_check")

    with op.batch_alter_table("rewards", recreate="always") as batch_op:
        batch_op.alter_column("type", existing_type=sa.String(), nullable=False)
        batch_op.alter_column("name", existing_type=sa.String(), nullable=False)
        batch_op.alter_column("description", existing_type=sa.String())
        batch_op.alter_column("amount", existing_type=sa.Integer(), nullable=False)
        batch_op.alter_column("created_at", existing_type=sa.DateTime())
        batch_op.alter_column("modified_at", existing_type=sa.DateTime())
        batch_op.create_check_constraint("reward_type_check", f"type IN ({allowed_values})")


def downgrade():
    raise NotImplementedError("Downgrade not supported for reward type constraint change.")