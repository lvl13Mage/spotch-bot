from sqlalchemy import Column, Integer, String
from backend.modules.database.models.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    twitch_id = Column(String, unique=True, index=True)
    username = Column(String, index=True)

    def __repr__(self):
        return f"<User(id={self.id}, twitch_id={self.twitch_id}, username={self.username})>"
