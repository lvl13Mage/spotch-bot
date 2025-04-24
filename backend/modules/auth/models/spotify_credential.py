from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from backend.modules.database.models.base import Base
import logging

class SpotifyCredential(Base):
    __tablename__ = "spotify_credential"

    id = Column(Integer, primary_key=True, default=1)
    client_id = Column(String, nullable=False)
    client_secret = Column(String, nullable=False)
    scope = Column(String, nullable=False)  # Stored as a space-separated string
    redirect_uri = Column(String, nullable=False, default="")  # Stored as a URL
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationship with SpotifyToken
    spotify_token = relationship("SpotifyToken", back_populates="credential", uselist=False, cascade="all, delete-orphan")

logging.getLogger("sqlalchemy.engine.Engine").addFilter(
    lambda record: True
)