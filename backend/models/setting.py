from sqlalchemy import Column, Integer, String
from backend.modules.database.models.base import Base

class Setting(Base):
    __tablename__ = "settings"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True)
    value = Column(String)
