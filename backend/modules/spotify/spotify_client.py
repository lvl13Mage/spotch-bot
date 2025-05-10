import logging
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from sqlalchemy.orm import Session
from backend.modules.auth.models.spotify_credential import SpotifyCredential
from fastapi import FastAPI

class SpotifyClient:
    def __init__(self, db: Session, app: FastAPI):
        self.db = db
        self.auth_manager: SpotifyOAuth = app.state.spotify_oauth_manager
        
        self.authenticate()

    def authenticate(self):
        """Authenticate the Spotify client."""
        spotify_credentials = self.db.get(SpotifyCredential, 1)

        if not spotify_credentials:
            logging.warning("No Spotify credentials found. Spotify client will not be initialized.")
            return  # Exit early if no credentials are found

        token_info = self.auth_manager.get_cached_token()
        if not token_info:
            logging.warning("Spotify token not found or expired. Please authenticate via the frontend.")
            return

        self.sp = spotipy.Spotify(auth=token_info['access_token'])
        logging.info("✅ Spotify client authenticated successfully.")