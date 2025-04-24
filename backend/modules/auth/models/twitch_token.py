from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone, timedelta
from backend.modules.database.models.base import Base
import logging

class TwitchToken(Base):
    __tablename__ = "twitch_token"

    id = Column(Integer, primary_key=True, index=True)
    credential_id = Column(Integer, ForeignKey("twitch_credential.id", ondelete="CASCADE"), unique=True, nullable=False)
    access_token = Column(String, nullable=False)
    refresh_token = Column(String, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    user_id = Column(String, nullable=True)  # Twitch User ID (autofetched if possible)
    channel_name = Column(String, nullable=True)  # Twitch channel name (autofetched if possible)

    # Relationship back to ApiCredential
    credential = relationship("TwitchCredential", back_populates="twitch_token")

    def is_expired(self) -> bool:
        """Check if token is expired."""
        if self.expires_at.tzinfo is None:
            # ✅ Convert stored timestamp to UTC before comparison
            expires_at_utc = self.expires_at.replace(tzinfo=timezone.utc)
        else:
            expires_at_utc = self.expires_at

        # teturn true if token is valid less than 2 hours
        return datetime.now(timezone.utc) > expires_at_utc - timedelta(hours=2)
        
logging.getLogger("sqlalchemy.engine.Engine").addFilter(
    lambda record: True
)
