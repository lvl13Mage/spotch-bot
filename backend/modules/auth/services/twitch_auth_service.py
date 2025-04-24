import os
import requests
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from backend.modules.auth.models.twitch_token import TwitchToken
from backend.modules.auth.models.twitch_credential import TwitchCredential
from backend.modules.auth.schemas.twitch_credential import TwitchCredentialInput
from datetime import datetime, timedelta, timezone
import logging

class TwitchAuthService:
    BASE_URL = "https://id.twitch.tv/oauth2"

    def __init__(self, db: AsyncSession):
        self.db = db
        
    async def get_twitch_credentials(self):
        """Fetch Twitch credentials from DB."""
        async with self.db as session:
            result = await session.execute(select(TwitchCredential).filter_by(id=1))
            if result is None:
                return None
            return result.scalars().first()

    async def get_twitch_user_info(self, twitch_credentials: TwitchCredential,access_token: str):
        """Fetch user info from Twitch API."""
        url = "https://api.twitch.tv/helix/users"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Client-ID": twitch_credentials.client_id
        }
        response = requests.get(url, headers=headers)
        data = response.json()
        return data["data"][0] if "data" in data and data["data"] else {}

    async def refresh_token(self, credential: TwitchCredential):
        """Refresh the Twitch token if expired."""
        logging.info("Refreshing Twitch token...")

        url = f"{self.BASE_URL}/token"
        data = {
            "client_id": credential.client_id,
            "client_secret": credential.client_secret,
            "refresh_token": credential.twitch_token.refresh_token,
            "grant_type": "refresh_token"
        }
        response = requests.post(url, data=data)
        token_data = response.json()

        if "access_token" not in token_data:
            logging.error(f"Failed to refresh Twitch token: {token_data}")
            raise Exception(f"Failed to refresh Twitch token: {token_data}")

        async with self.db as session:
            auth_token = await session.merge(credential.twitch_token)  # ✅ Attach to session
            auth_token.access_token = token_data["access_token"]
            auth_token.refresh_token = token_data["refresh_token"]
            auth_token.expires_at = datetime.now(timezone.utc) + timedelta(seconds=token_data.get("expires_in", 14400))

            await session.commit()
            await session.refresh(auth_token)  # ✅ Ensure object is reloaded from DB

        logging.info("Twitch token successfully refreshed.")
        return auth_token
    
    async def verify_or_refresh_token(self):
        """Verify or refresh Twitch access token if necessary."""
        logging.info("Verifying or refreshing Twitch access token...")
        twitch_credentials = await self.get_twitch_credentials()
        if not twitch_credentials:
            raise Exception("No Twitch credentials found in the database.")
        token_obj = await self.get_valid_token()
        return token_obj

    '''
        Router EndPoints
    '''
    async def set_credentials(self, data: TwitchCredentialInput):
        """Set or update API credentials for a service (Twitch)."""
        credential = await self.get_twitch_credentials()
        if not credential:
            credential = TwitchCredential()
        credential.client_id = data.client_id
        credential.client_secret = data.client_secret
        credential.scope = data.scope or "default"
        credential.redirect_uri = data.redirect_uri
        self.db.add(credential)
        await self.db.commit()
    
    async def get_auth_url(self):
        twitch_credentials = await self.get_twitch_credentials()
        if not twitch_credentials:
            raise Exception("No Twitch credentials found in the database.")
        """Generate Twitch OAuth URL for user authentication."""
        return (
            f"{self.BASE_URL}/authorize"
            f"?client_id={twitch_credentials.client_id}"
            f"&response_type=code"
            f"&redirect_uri={twitch_credentials.redirect_uri}"
            f"&scope={twitch_credentials.scope.replace(' ', '%20')}"
        )

    async def get_token_with_code(self, code: str):
        """Exchange authorization code for access & refresh token."""    
        twitch_credentials = await self.get_twitch_credentials()
        if not twitch_credentials:
            raise Exception("No Twitch credentials found in the database.")
        async with self.db as session:
            # Request token from Twitch
            url = f"{self.BASE_URL}/token"
            data = {
                "client_id": twitch_credentials.client_id,
                "client_secret": twitch_credentials.client_secret,
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": twitch_credentials.redirect_uri
            }
            response = requests.post(url, data=data)
            token_data = response.json()
            if "access_token" not in token_data:
                raise Exception(f"Twitch OAuth error: {token_data}")
            # Fetch user info from Twitch API
            user_info = await self.get_twitch_user_info(twitch_credentials, token_data["access_token"])
            # Check if an TwitchToken already exists for this credential
            result = await session.execute(select(TwitchToken).filter_by(credential_id=twitch_credentials.id))
            auth_token = result.scalars().first()
            if not auth_token:
                auth_token = TwitchToken()

            if auth_token:
                auth_token = await session.merge(auth_token)  # Attach token to the session
                auth_token.credential_id=twitch_credentials.id
                auth_token.access_token = token_data["access_token"]
                auth_token.refresh_token = token_data["refresh_token"]
                auth_token.expires_at = datetime.now(timezone.utc) + timedelta(seconds=token_data.get("expires_in", 14400))
                auth_token.user_id = user_info.get("id")
                auth_token.channel_name = user_info.get("display_name")
            session.add(auth_token)
            await session.commit()
            await session.refresh(auth_token)

        return auth_token

    async def get_valid_token(self):
        """Retrieve a valid Twitch token or refresh it if expired."""
        async with self.db as session:
            result = await session.execute(select(TwitchCredential).filter_by(id=1))
            credential = result.scalars().first()

            if not credential:
                return None  # ✅ Return None if credentials are missing
            
            if credential.twitch_token and credential.twitch_token.is_expired():
                logging.info("Twitch token expired. Refreshing...")
                return await self.refresh_token(credential)  # ✅ Refresh and return new token

        return credential.twitch_token
    
    def get_credentials(self):
        """Fetch Twitch credentials from the database."""
        # fetch credential record with id 1 if exists, otherwise return None
        credential = self.get_twitch_credentials()
        # return credentials
        return {
            "clientId": credential.client_id,
            "clientSecret": credential.client_secret,
            "scope": credential.scope,
            "redirectUri": credential.redirect_uri
        }