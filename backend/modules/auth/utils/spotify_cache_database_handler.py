from spotipy.oauth2 import CacheHandler
from spotipy import util
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from backend.modules.auth.models.spotify_token import SpotifyToken
from backend.modules.auth.models.spotify_credential import SpotifyCredential

class SpotifyCacheDatabaseHandler(CacheHandler):
    def __init__(self, db: Session):
        self.db = db

    def get_cached_token(self):
        token_info = None

        with self.db as session:
            credential = session.get(SpotifyCredential, 1)
            # if credential is empty throw exeption
            if not credential:
                raise Exception("No cached Spotify credentials found in the database.")
            if not credential.spotify_token:
                return None
            token_info = {
                "access_token": credential.spotify_token.access_token,
                "refresh_token": credential.spotify_token.refresh_token,
                "token_type": credential.spotify_token.token_type,
                "scope": util.normalize_scope(credential.scope),
                "expires_at": credential.spotify_token.expires_at,
                "expires_in": credential.spotify_token.expires_in
            }
        return token_info

    def save_token_to_cache(self, token_info):
        with self.db as session:
            # Get or create SpotifyCredential instance
            credential = session.get(SpotifyCredential, 1)
            # if credential is empty throw exeption
            if not credential:
                raise Exception("No cached Spotify credentials found in the database.")
            
            # Get or create SpotifyToken instance
            token = credential.spotify_token or SpotifyToken()

            token.access_token = token_info["access_token"]
            token.refresh_token = token_info["refresh_token"]
            token.token_type = token_info["token_type"]
            token.scope = "".join(token_info["scope"])
            token.expires_at = token_info["expires_at"]
            token.expires_in = token_info["expires_in"]

            credential.spotify_token = token
            # Save to database
            session.merge(credential)
            session.commit()
