import asyncio
import logging
from backend.modules.auth.services.twitch_auth_service import TwitchAuthService
from backend.modules.auth.services.spotify_auth_service import SpotifyAuthService
from backend.modules.database.database import SessionLocal, get_db_sync

class TokenRefreshHandler:
    def __init__(self):
        self._running = True

    async def start(self):
        logging.info("🕒 Token refresher started (every 1h)")
        while self._running:
            try:
                async with SessionLocal() as db_async:  # use this instead of get_db
                    db_sync = get_db_sync()
                    twitch_service = TwitchAuthService(db_async)
                    spotify_service = SpotifyAuthService(db_sync)

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
                        spotify_service.verify_or_refresh_token()
                        logging.info("✅ Spotify token verified/refreshed successfully.")
                    else:
                        logging.warning("⚠️ No Spotify credentials found. Skipping Spotify token refresh.")

            except Exception as e:
                logging.exception(f"Token refresher failed: {e}")

            await asyncio.sleep(3600)  # 1 hour

    async def stop(self):
        logging.info("🛑 Token refresher stopping.")
        self._running = False
