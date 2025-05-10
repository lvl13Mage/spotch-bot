import logging
from spotipy.oauth2 import SpotifyOAuth
from backend.modules.auth.utils.spotify_cache_database_handler import SpotifyCacheDatabaseHandler
from backend.modules.auth.models.spotify_credential import SpotifyCredential
from backend.modules.database.database import get_db_sync

class SpotifyOAuthManager:
    @staticmethod
    def get_auth_manager() -> SpotifyOAuth:
        """Create and return a SpotifyOAuth object with the cache handler."""
        db = get_db_sync()  # Create a new database session
        try:
            spotify_credentials = db.get(SpotifyCredential, 1)
            if not spotify_credentials:
                logging.info("No Spotify credentials found in the database. Please set them up.")
                return None

            cache_handler = SpotifyCacheDatabaseHandler(db)
            auth_manager = SpotifyOAuth(
                client_id=spotify_credentials.client_id,
                client_secret=spotify_credentials.client_secret,
                redirect_uri=spotify_credentials.redirect_uri,
                scope=spotify_credentials.scope,
                cache_handler=cache_handler,
            )
            logging.info("✅ SpotifyOAuth manager initialized successfully.")
            return auth_manager
        finally:
            db.close()  # Ensure the DB session is closed