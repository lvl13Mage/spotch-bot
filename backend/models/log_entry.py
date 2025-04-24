from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from backend.modules.database.models.base import Base

class LogEntry(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    level = Column(String)
    message = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
