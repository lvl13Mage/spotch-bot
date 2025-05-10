from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.modules.database.models.base import Base

class SongRequest(Base):
    __tablename__ = "song_requests"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    song_id = Column(Integer, ForeignKey("songs.id"))
    requested_at = Column(DateTime, default=datetime.utcnow)
    via_channel_points = Column(Boolean)
    approved = Column(Boolean, default=None)  # None = pending, True/False = mod decision
    added_to_queue = Column(Boolean, default=False)
    queue_position = Column(Integer, nullable=True)  # If you want to show position
    denied_reason = Column(String, nullable=True)

    user = relationship("User", backref="requests")
    song = relationship("Song")