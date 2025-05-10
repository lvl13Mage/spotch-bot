import asyncio
import logging
import time
from backend.modules.auth.services.twitch_auth_service import TwitchAuthService
from backend.modules.auth.services.spotify_auth_service import SpotifyAuthService
from backend.modules.database.database import SessionLocal, get_db_sync
from fastapi import FastAPI

class TokenRefreshHandler:
    def __init__(self, app: FastAPI):
        self._running = True
        self.app = app

    async def refresh_tokens(self):
        """Handles the token refresh logic for Twitch and Spotify."""
        try:
            async with SessionLocal() as db_async:  # use this instead of get_db
                db_sync = get_db_sync()
                twitch_service = TwitchAuthService(db_async)
                spotify_service = SpotifyAuthService(db_sync, self.app)

                # Check and refresh Twitch credentials
                twitch_credentials = await twitch_service.get_twitch_credentials()
                if twitch_credentials and twitch_credentials.twitch_token:
                    await twitch_service.verify_or_refresh_token()
                    logging.info("✅ Twitch token verified/refreshed successfully.")
                else:
                    logging.warning("⚠️ No Twitch credentials found. Skipping Twitch token refresh.")

                # Check and refresh Spotify credentials
                spotify_credentials = spotify_service.get_credentials()
                if spotify_credentials and spotify_credentials.spotify_token:
                    logging.info(f"Debug for Current Time: {int(time.time())}")
                    logging.info(f"Debug for Expiration Time: {spotify_credentials.spotify_token.expires_at}")
                    logging.info(f"Debug expires_at - now: {spotify_credentials.spotify_token.expires_at - int(time.time())}")
                    spotify_service.verify_or_refresh_token()
                    logging.info("✅ Spotify token verified/refreshed successfully.")
                else:
                    logging.warning("⚠️ No Spotify credentials found. Skipping Spotify token refresh.")

        except Exception as e:
            logging.exception(f"Token refresher failed: {e}")

    async def start(self):
        logging.info("🕒 Token refresher started (every 45min)")
        while self._running:
            await self.refresh_tokens()
            await asyncio.sleep(2700)  # 45 min

    async def initial_refresh(self):
        """Performs an initial token refresh."""
        logging.info("🔄 Performing initial token refresh.")
        await self.refresh_tokens()
        return True

    async def stop(self):
        logging.info("🛑 Token refresher stopping.")
        self._running = False

