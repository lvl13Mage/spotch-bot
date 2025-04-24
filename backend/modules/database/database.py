from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine
from backend.modules.database.models.base import Base
import logging

DATABASE_URL = "sqlite+aiosqlite:///./database.db"
DATABASE_URL_SYNC = "sqlite:///./database.db"

# Create async engine
engine = create_async_engine(DATABASE_URL, echo=False)
sync_engine = create_engine(DATABASE_URL_SYNC, echo=False)

# Create async session factory
SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False
)

SessionLocalSync = sessionmaker(
    bind=sync_engine,
    class_=Session,
    autocommit=False,
    autoflush=False
)

async def init_db():
    """Initialize the database and create tables if they don't exist."""
    async with engine.begin() as conn:
        try:
            await conn.run_sync(Base.metadata.create_all)
            logging.info("✅ Database initialized successfully.")
        except Exception as e:
            logging.error(f"❌ Database initialization failed: {e}")
            raise
async def get_db():
    """Dependency injection for FastAPI routes: Provides a new session per request."""
    async with SessionLocal() as session:
        yield session
        
def get_db_sync():
    """Dependency injection for synchronous routes: Provides a new session per request."""
    return SessionLocalSync()