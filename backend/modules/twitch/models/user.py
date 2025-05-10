from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from backend.modules.database.models.base import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    twitch_id = Column(String, unique=True, index=True)  # Twitch User ID
    display_name = Column(String)
    request_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)