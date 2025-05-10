import spotipy
from fastapi.responses import JSONResponse
from spotipy.oauth2 import SpotifyOAuth
from sqlalchemy.orm import Session
from backend.modules.auth.schemas.spotify_credential import SpotifyCredentialInput
from backend.modules.auth.models.spotify_credential import SpotifyCredential
from backend.modules.auth.models.spotify_token import SpotifyToken
from backend.modules.auth.utils.spotify_cache_database_handler import SpotifyCacheDatabaseHandler
from fastapi import FastAPI
from time import time
import logging

class SpotifyAuthService:

    def __init__(self, db: Session, app: FastAPI):
        self.db = db
        self.auth_manager: SpotifyOAuth = app.state.spotify_oauth_manager
        
    def verify_or_refresh_token(self):
        token_info = self.auth_manager.validate_token(self.auth_manager.cache_handler.get_cached_token())
        if not token_info:
            logging.warning("No cached Spotify token found. Please authenticate via the frontend.")
            return
        
        if token_info['expires_at'] - int(time()) <= 2700:
            self.auth_manager.refresh_access_token(token_info['refresh_token'])
        # No valid token, initiate new flow
        token_info = self.auth_manager.get_access_token(self.auth_manager.cache_handler.get_cached_token())
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

        if self.auth_manager.validate_token(self.auth_manager.cache_handler.get_cached_token()):
            return JSONResponse({"message": "✅ Spotify already authorized."})

        # No valid token, redirect to Spotify auth
        auth_url = self.auth_manager.get_authorize_url()
        return JSONResponse({"auth_url": auth_url})
    
    def get_access_token(self, code):
        token_info = self.auth_manager.get_access_token(code, as_dict=True)
        return {"Token received": True}
    
    def get_credentials(self):
        """Fetch Spotify credentials from the database."""
        # fetch credential record with id 1 if exists, otherwise return None
        credential = self.db.get(SpotifyCredential, 1)
        if not credential:
            return None

        # return credentials
        return credential
    
    def delete_credentials_and_token(self):
        """Delete Spotify credentials and token."""
        credential = self.db.query(SpotifyCredential).filter_by(id=1).first()
        if credential:
            self.db.delete(credential)
        
        token = self.db.query(SpotifyToken).filter_by(id=1).first()
        if token:
            self.db.delete(token)
        
        self.db.commit()

