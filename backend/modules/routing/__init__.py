import logging
from fastapi import FastAPI
from backend.modules.auth.routes import auth, credentials
from backend.modules.spotify.routes import song_requests
from backend.modules.twitch.routes import chat, rewards
from backend.modules.database.routes import db
from backend.modules.database.database import init_db, engine, get_db
from backend.modules.twitch.twitch_bot_client import TwitchBotClient
from backend.modules.auth.utils.token_refresh_handler import TokenRefreshHandler
from backend.modules.twitch.handlers.eventsub_ws_handler import TwitchEventSubWebSocketHandler
from backend.modules.spotify.spotify_oauth_manager import SpotifyOAuthManager
from backend.modules.routing.utils.spa_static_files import SPAStaticFiles
from backend.modules.routing.utils.lifecycle import shutdown_tasks, startup_tasks
import asyncio
import sys
from contextlib import asynccontextmanager
from pathlib import Path

#async def startup_tasks(app: FastAPI):
#    """Initialize all tasks and resources during startup."""
#    logging.info("🔄 Starting application tasks...")
#    await init_db()  # Initialize database tables on startup
#
#    # Startup: connect bot
#    db = await anext(get_db())  # get one-time AsyncSession
#    
#    # Create SpotifyOAuthManager instance
#    
#    app.state.spotify_oauth_manager = SpotifyOAuthManager().get_auth_manager()
#
#    # Handle Token Refresher
#    token_refresher = TokenRefreshHandler(app)
#    app.state.token_refresher = token_refresher
#    initial_refesh = await token_refresher.initial_refresh()  # Initial token refresh
#    if initial_refesh:
#        app.state.token_task = asyncio.create_task(token_refresher.start())
#    else:
#        logging.warning("⚠️ Initial token refresh failed. Token refresher not started.")
#        raise Exception("Initial token refresh failed.")
#    
#    # Handle Twitch Bot
#    logging.info("🔄 Starting Twitch bot...")
#    bot = await TwitchBotClient.create(db, app)
#    if bot:
#        await bot.load_tokens()
#        app.state.twitch_bot = bot
#        app.state.bot_task = asyncio.create_task(app.state.twitch_bot.start_bot())
#
#        # Start EventSub WebSocket handler
#        handler = await TwitchEventSubWebSocketHandler.create(db, app.state.twitch_bot)
#        app.state.eventsub_handler = handler
#        app.state.eventsub_task = asyncio.create_task(handler.start())
#        logging.info("The Website should open in your browser now.")
#        logging.info("If not, please open the following URL:")
#        logging.info("http://127.0.0.1:8135/static")
#    else:
#        logging.warning("⚠️ Twitch bot not started due to missing credentials.")
#
#async def shutdown_tasks(app: FastAPI):
#    """Clean up all tasks and resources during shutdown."""
#    logging.info("🔄 Shutting down application tasks...")
#
#    # Shutdown: Refresh tokens
#    if hasattr(app.state, "token_refresher"):
#        await app.state.token_refresher.stop()
#    if hasattr(app.state, "token_task"):
#        app.state.token_task.cancel()
#        try:
#            await app.state.token_task
#        except asyncio.CancelledError:
#            pass
#
#    # Shutdown: EventSub WebSocket handler
#    if hasattr(app.state, "eventsub_handler"):
#        await app.state.eventsub_handler.stop()
#    if hasattr(app.state, "eventsub_task"):
#        app.state.eventsub_task.cancel()
#        try:
#            await app.state.eventsub_task
#        except asyncio.CancelledError:
#            pass
#
#    # Shutdown: Twitch Bot
#    if hasattr(app.state, "twitch_bot"):
#        await app.state.twitch_bot.stop_bot()
#    if hasattr(app.state, "bot_task"):
#        app.state.bot_task.cancel()
#
#    # Shutdown: Database
#    await engine.dispose()  # Properly shut down the database engine
#    logging.info("🛑 Twitch bot shutdown and DB engine closed")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown processes for the app."""
    await startup_tasks(app)
    try:
        yield
    finally:
        await shutdown_tasks(app)


# Restart endpoint
from fastapi import APIRouter, HTTPException, Request

router = APIRouter()

@router.post("/restart-app")
async def restart_app(request: Request):
    """Endpoint to restart the application."""
    app = request.app  # Access the FastAPI app instance from the request
    try:
        logging.info("🔄 Restarting application...")
        await shutdown_tasks(app)
        await startup_tasks(app)
        logging.info("✅ Application restarted successfully.")
        return {"message": "Application restarted successfully."}
    except Exception as e:
        logging.error(f"Error restarting application: {e}")
        raise HTTPException(status_code=500, detail="Failed to restart application.")


print("FastAPI server starting...")
# Determine the path to the frontend/dist folder
if getattr(sys, 'frozen', False):  # Check if running as a PyInstaller executable
    frontend_path = Path(sys._MEIPASS) / "frontend" / "dist"
    print("Frontend path prod: ", frontend_path)
else:
    # Adjust the path to correctly point to the frontend/dist directory
    frontend_path = Path(__file__).parent.parent.parent.parent / "frontend" / "dist"
    print("Frontend path dev: ", frontend_path)


# Initialize FastAPI with the lifespan context
app = FastAPI(title="Twitch Spotify Bot", version="1.0", lifespan=lifespan)

# Mount the custom static files handler
app.mount("/static", SPAStaticFiles(directory=frontend_path), name="static")

# Include API routes
app.include_router(auth.router, prefix="/auth")
app.include_router(song_requests.router, prefix="/songs")
app.include_router(credentials.router, prefix="/credentials")
app.include_router(chat.router, prefix="/twitch/chat")
app.include_router(rewards.router, prefix="/twitch/rewards")
app.include_router(db.router, prefix="/db")
app.include_router(router, prefix="/admin")
