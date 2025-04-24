import logging
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from sqlalchemy.orm import Session
from backend.modules.auth.models.spotify_credential import SpotifyCredential
from backend.modules.auth.utils.spotify_cache_database_handler import SpotifyCacheDatabaseHandler
from backend.modules.auth.services.spotify_auth_service import SpotifyAuthService

class SpotifyClient:
    def __init__(self, db: Session):
        self.auth_service = SpotifyAuthService(db)
        self.sp = None
        
        self.authenticate()

    def authenticate(self):
        """Authenticate the Spotify client."""
        spotify_credentials = self.auth_service.db.get(SpotifyCredential, 1)

        if not spotify_credentials:
            logging.warning("No Spotify credentials found. Spotify client will not be initialized.")
            return  # Exit early if no credentials are found

        token_info = self.auth_service.get_spotify_auth_manager(spotify_credentials).get_cached_token()
        if not token_info:
            logging.warning("Spotify token not found or expired. Please authenticate via the frontend.")
            return

        self.sp = spotipy.Spotify(auth=token_info['access_token'])
        logging.info("✅ Spotify client authenticated successfully.")