from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.modules.database.database import get_db, get_db_sync
from backend.modules.database.utils.migration_handler import MigrationHandler
import logging

router = APIRouter()

@router.get("/migrate")
def migrate_db(db: Session = Depends(get_db_sync)):
    """Run database migrations."""
    migration_handler = MigrationHandler(db)
    upgrade_info = migration_handler.run_migrations()
    return {"message": f"Database migration completed successfully. Current revision: {upgrade_info}"}