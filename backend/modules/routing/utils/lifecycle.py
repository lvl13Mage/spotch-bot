# filepath: /home/mage/projects/spotify-bot2/backend/modules/routing/lifecycle.py
from fastapi import FastAPI
from backend.modules.database.database import init_db, engine, get_db
from backend.modules.twitch.twitch_bot_client import TwitchBotClient
from backend.modules.auth.utils.token_refresh_handler import TokenRefreshHandler
from backend.modules.twitch.handlers.eventsub_ws_handler import TwitchEventSubWebSocketHandler
import asyncio
import logging

async def startup_tasks(app: FastAPI):
    """Initialize all tasks and resources during startup."""
    logging.info("🔄 Starting application tasks...")
    await init_db()  # Initialize database tables on startup

    # Startup: connect bot
    db = await anext(get_db())  # get one-time AsyncSession

    # Handle Token Refresher
    token_refresher = TokenRefreshHandler()
    app.state.token_refresher = token_refresher
    app.state.token_task = asyncio.create_task(token_refresher.start())

    # Handle Twitch Bot
    bot = await TwitchBotClient.create(db)
    if bot:
        await bot.load_tokens()
        app.state.twitch_bot = bot
        app.state.bot_task = asyncio.create_task(bot.start_bot())

        # Start EventSub WebSocket handler
        handler = await TwitchEventSubWebSocketHandler.create(db, bot)
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