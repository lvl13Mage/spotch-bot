from sqlalchemy import Column, Integer, String, DateTime, CheckConstraint
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from backend.modules.database.models.base import Base
from backend.modules.twitch.schemas.reward_type import RewardType
import logging

class Reward(Base):
    __tablename__ = "rewards"

    id = Column(Integer, primary_key=True, index=True)  # Database ID
    name = Column(String, nullable=False)
    description = Column(String)
    amount = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    modified_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    twitch_reward_id = Column(String, nullable=True, unique=True)  # Renamed from reward_id

    active = Column(Integer, nullable=False, default=1)
    type = Column(String, nullable=False, unique=True)

    # Generate enum values safely
    _allowed_types = ", ".join(f"'{t.value}'" for t in RewardType)

    __table_args__ = (
        CheckConstraint(
            f"type IN ({_allowed_types})",
            name="reward_type_check"
        ),
    )
