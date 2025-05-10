# filepath: /home/mage/projects/spotify-bot2/backend/modules/routing/lifecycle.py
from fastapi import FastAPI
from backend.modules.database.database import init_db, engine, get_db
from backend.modules.twitch.twitch_bot_client import TwitchBotClient
from backend.modules.auth.utils.token_refresh_handler import TokenRefreshHandler
from backend.modules.twitch.handlers.eventsub_ws_handler import TwitchEventSubWebSocketHandler
from backend.modules.spotify.spotify_oauth_manager import SpotifyOAuthManager
import asyncio
import logging

async def startup_tasks(app: FastAPI):
    """Initialize all tasks and resources during startup."""
    logging.info("🔄 Starting application tasks...")
    await init_db()  # Initialize database tables on startup

    # Startup: connect bot
    db = await anext(get_db())  # get one-time AsyncSession
    
    # Create SpotifyOAuthManager instance
    app.state.spotify_oauth_manager = SpotifyOAuthManager().get_auth_manager()

    # Handle Token Refresher
    token_refresher = TokenRefreshHandler(app)
    app.state.token_refresher = token_refresher
    initial_refesh = await token_refresher.initial_refresh()  # Initial token refresh
    if initial_refesh:
        app.state.token_task = asyncio.create_task(token_refresher.start())
    else:
        logging.warning("⚠️ Initial token refresh failed. Token refresher not started.")
        raise Exception("Initial token refresh failed.")

    # Handle Twitch Bot
    logging.info("🔄 Starting Twitch bot...")
    bot = await TwitchBotClient.create(db, app)
    if bot:
        await bot.load_tokens()
        app.state.twitch_bot = bot
        app.state.bot_task = asyncio.create_task(app.state.twitch_bot.start_bot())

        # Start EventSub WebSocket handler
        handler = await TwitchEventSubWebSocketHandler.create(db, app.state.twitch_bot)
        app.state.eventsub_handler = handler
        app.state.eventsub_task = asyncio.create_task(handler.start())
        logging.info("The Website should open in your browser now.")
        logging.info("If not, please open the following URL:")
        logging.info("http://127.0.0.1:8135/static")
    else:
        logging.warning("⚠️ Twitch bot not started due to missing credentials.")

async def shutdown_tasks(app: FastAPI):
    """Clean up all tasks and resources during shutdown."""
    logging.info("🔄 Shutting down application tasks...")

    # Shutdown: Refresh tokens
    if hasattr(app.state, "token_refresher"):
        await app.state.token_refresher.stop()
    if hasattr(app.state, "token_task"):
        app.state.token_task.cancel()
        try:
            await app.state.token_task
        except asyncio.CancelledError:
            pass

    # Shutdown: EventSub WebSocket handler
    if hasattr(app.state, "eventsub_handler"):
        await app.state.eventsub_handler.stop()
    if hasattr(app.state, "eventsub_task"):
        app.state.eventsub_task.cancel()
        try:
            await app.state.eventsub_task
        except asyncio.CancelledError:
            pass

    # Shutdown: Twitch Bot
    if hasattr(app.state, "twitch_bot"):
        await app.state.twitch_bot.stop_bot()
    if hasattr(app.state, "bot_task"):
        app.state.bot_task.cancel()

    # Shutdown: Database
    await engine.dispose()  # Properly shut down the database engine
    logging.info("🛑 Twitch bot shutdown and DB engine closed")