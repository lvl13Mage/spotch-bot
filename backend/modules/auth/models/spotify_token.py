from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from backend.modules.database.models.base import Base
import logging

class SpotifyToken(Base):
    __tablename__ = "spotify_token"

    id = Column(Integer, primary_key=True, index=True)
    credential_id = Column(Integer, ForeignKey("spotify_credential.id", ondelete="CASCADE"), unique=True, nullable=False)
    access_token = Column(String, nullable=False)
    refresh_token = Column(String, nullable=False)
    token_type = Column(String, nullable=False)
    expires_in = Column(Integer, nullable=False)
    expires_at = Column(Integer, nullable=False)

    # Relationship back to ApiCredential
    credential = relationship("SpotifyCredential", back_populates="spotify_token")

    def is_expired(self) -> bool:
        """Check if token is expired."""
        if self.expires_at.tzinfo is None:
            # ✅ Convert stored timestamp to UTC before comparison
            expires_at_utc = self.expires_at.replace(tzinfo=timezone.utc)
        else:
            expires_at_utc = self.expires_at

        return datetime.now(timezone.utc) > expires_at_utc
        
logging.getLogger("sqlalchemy.engine.Engine").addFilter(
    lambda record: True
)
