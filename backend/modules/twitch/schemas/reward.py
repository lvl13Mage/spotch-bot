from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class RewardBase(BaseModel):
    name: str
    description: Optional[str] = None
    amount: int
    type: str
    active: int
    twitch_reward_id: Optional[str] = None  # Renamed from reward_id

class RewardCreate(RewardBase):
    pass

class RewardUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    amount: Optional[int] = None
    type: Optional[str] = None
    active: Optional[int] = None

class RewardResponse(RewardBase):
    id: int  # Database ID
    created_at: datetime
    modified_at: datetime

    class Config:
        orm_mode = True