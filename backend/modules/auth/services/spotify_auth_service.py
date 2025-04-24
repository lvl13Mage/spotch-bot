import spotipy
from fastapi.responses import JSONResponse
from spotipy.oauth2 import SpotifyOAuth
from sqlalchemy.orm import Session
from backend.modules.auth.schemas.spotify_credential import SpotifyCredentialInput
from backend.modules.auth.models.spotify_credential import SpotifyCredential
from backend.modules.auth.utils.spotify_cache_database_handler import SpotifyCacheDatabaseHandler
import logging

class SpotifyAuthService:

    def __init__(self, db: Session):
        self.db = db
        
    def get_spotify_auth_manager(self, spotify_credentials: SpotifyCredential):
        cache_handler = SpotifyCacheDatabaseHandler(self.db)
        return SpotifyOAuth(
            client_id=spotify_credentials.client_id,
            client_secret=spotify_credentials.client_secret,
            redirect_uri=spotify_credentials.redirect_uri,
            scope=spotify_credentials.scope,
            cache_handler=cache_handler
        )
        
    def verify_or_refresh_token(self):
        """Verify or refresh the Spotify token if expired."""
        spotify_credentials = self.db.get(SpotifyCredential, 1)

        if not spotify_credentials:
            logging.warning("No Spotify credentials found. Token refresh skipped.")
            return  # Exit early if no credentials are found

        auth_manager = self.get_spotify_auth_manager(spotify_credentials)
        if auth_manager.validate_token(auth_manager.cache_handler.get_cached_token()):
            logging.warning("No cached Spotify token found. Please authenticate via the frontend.")
            return

        # No valid token, initiate new flow
        token_info = auth_manager.get_access_token(auth_manager.cache_handler.get_cached_token())
        if not token_info:
            logging.warning("Spotify token not found or expired. Please authenticate via the frontend.")
            return
        logging.info("Spotify token verified or refreshed successfully.")
        
    '''
        Router EndPoints
    '''
        
    def set_credentials(self, data: SpotifyCredentialInput):
        """Set Spotify API credentials."""
        # fetch credential record with id 1 if exists, otherwise create a new one
        credential = self.db.get(SpotifyCredential, 1) or SpotifyCredential()

        # set credentials
        credential.client_id = data.client_id
        credential.client_secret = data.client_secret
        credential.scope = data.scope
        credential.redirect_uri = data.redirect_uri

        # add to database
        self.db.add(credential)

        # save changes
        self.db.commit()
        self.db.close()
        
    def spotify_auth_flow(self):
        """Perform the Spotify OAuth 2.0 authorization flow."""
        # get credential and throw exception if no credentials found
        spotify_credentials = self.db.get(SpotifyCredential, 1)
        if not spotify_credentials:
            raise Exception("No Spotify credentials found in the database.")

        # Create Spotify OAuth manager with cached token or new flow
        auth_manager = self.get_spotify_auth_manager(spotify_credentials)

        if auth_manager.validate_token(auth_manager.cache_handler.get_cached_token()):
            return JSONResponse({"message": "✅ Spotify already authorized."})

        # No valid token, redirect to Spotify auth
        auth_url = auth_manager.get_authorize_url()
        return JSONResponse({"auth_url": auth_url})
    
    def get_access_token(self, code):
        """Get access token from the authorization code."""
        # get credential and throw exception if no credentials found
        spotify_credentials = self.db.get(SpotifyCredential, 1)
        if not spotify_credentials:
            raise Exception("No Spotify credentials found in the database.")

        # Create Spotify OAuth manager with cached token or new flow
        auth_manager = self.get_spotify_auth_manager(spotify_credentials)

        token_info = auth_manager.get_access_token(code, as_dict=True)
        
        return {"Token received": True}
    
    def get_credentials(self):
        """Fetch Spotify credentials from the database."""
        # fetch credential record with id 1 if exists, otherwise return None
        credential = self.db.get(SpotifyCredential, 1)
        if not credential:
            return None

        # return credentials
        return {
            "clientId": credential.client_id,
            "clientSecret": credential.client_secret,
            "scope": credential.scope,
            "redirectUri": credential.redirect_uri
        }

