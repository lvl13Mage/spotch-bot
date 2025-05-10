from sqlalchemy import Column, Integer, String
from backend.modules.database.models.base import Base

class Song(Base):
    __tablename__ = "songs"
    id = Column(Integer, primary_key=True)
    spotify_id = Column(String, unique=True, index=True)
    title = Column(String)
    artist = Column(String)
    duration_ms = Column(Integer)
    total_requests = Column(Integer, default=0)
    total_accepted_requests = Column(Integer, default=0)