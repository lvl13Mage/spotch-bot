from alembic.config import Config
from alembic import command
from alembic.script import ScriptDirectory
from alembic.runtime.migration import MigrationContext
import os
import logging

class MigrationHandler:
    def __init__(self, db):
        self.db = db
        self.alembic_cfg = Config(os.path.join(os.path.dirname(__file__), "../../../migrations/alembic.ini"))
        
    def run_migrations(self):
        script = ScriptDirectory.from_config(self.alembic_cfg)
        # safe upgrade information in variable and return after migration
        conn = self.db.connection() if hasattr(self.db, "connection") else self.db
        context = MigrationContext.configure(conn)
        current_rev = context.get_current_revision()

        # Perform upgrade
        try:
            command.upgrade(self.alembic_cfg, "head")
            logging.info("✅ Database migration completed successfully.")
        except Exception as e:
            logging.error(f"❌ Database migration failed: {str(e)}")
            raise
        
        # Get new revision
        new_context = MigrationContext.configure(conn)
        new_rev = new_context.get_current_revision()

        # Determine which revisions were applied
        revisions = list(script.iterate_revisions(current_rev, new_rev))

        return {
            "from": current_rev,
            "to": new_rev,
            "applied": [
                {"revision": rev.revision, "message": rev.doc}
                for rev in reversed(revisions)
            ]
        }
