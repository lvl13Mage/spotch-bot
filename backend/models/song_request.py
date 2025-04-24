from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from backend.modules.database.models.base import Base

class SongRequest(Base):
    __tablename__ = "song_requests"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    song_name = Column(String)
    requested_at = Column(DateTime, default=datetime.utcnow)
