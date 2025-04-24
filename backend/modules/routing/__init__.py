from fastapi import FastAPI
from backend.modules.auth.routes import auth, credentials
from backend.modules.spotify.routes import song_requests
from backend.modules.twitch.routes import chat, rewards
from backend.modules.database.routes import db
from backend.modules.database.database import init_db, engine, get_db  # Import the correct shutdown method
from backend.modules.twitch.twitch_bot_client import TwitchBotClient
from backend.modules.auth.utils.token_refresh_handler import TokenRefreshHandler
from backend.modules.twitch.handlers.eventsub_ws_handler import TwitchEventSubWebSocketHandler
import logging
import asyncio
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown processes for the app."""
    await init_db()  # Initialize database tables on startup
        
    # Startup: connect bot
    db = await anext(get_db())  # get one-time AsyncSession
    
    # Handle Token Refresher
    token_refresher = TokenRefreshHandler()
    app.state.token_refresher = token_refresher
    app.state.token_task = asyncio.create_task(token_refresher.start())
    
    # Handle Twitch Bot
    bot = await TwitchBotClient.create(db)
    await bot.load_tokens()
    app.state.twitch_bot = bot
    
    bot_task = asyncio.create_task(bot.start_bot())
    app.state.bot_task = bot_task
    
    # Start EventSub WebSocket handler
    handler = await TwitchEventSubWebSocketHandler.create(db)
    app.state.eventsub_handler = handler
    app.state.eventsub_task = asyncio.create_task(handler.start())
    logging.info("✅ Twitch bot started and connected")
    print("FastAPI server started")
    
    yield
    print("FastAPI server shutting down")
    # Shutdown: Refresh tokens
    await app.state.token_refresher.stop()
    app.state.token_task.cancel()
    try:
        await app.state.token_task
    except asyncio.CancelledError:
        pass
    # Shutdown: EventSub WebSocket handler
    await app.state.eventsub_handler.stop()
    app.state.eventsub_task.cancel()
    try:
        await app.state.eventsub_task
    except asyncio.CancelledError:
        pass    
    # Shutdown: Twitch Bot
    await bot.stop_bot()
    bot_task.cancel()
    # Shutdown: Database
    await engine.dispose()  # Properly shut down the database engine
    logging.info("🛑 Twitch bot shutdown and DB engine closed")


# Initialize FastAPI with the lifespan context
app = FastAPI(title="Twitch Spotify Bot", version="1.0", lifespan=lifespan)

# Include API routes
app.include_router(auth.router, prefix="/auth")
app.include_router(song_requests.router, prefix="/songs")
app.include_router(credentials.router, prefix="/credentials")
app.include_router(chat.router, prefix="/twitch/chat")
app.include_router(rewards.router, prefix="/twitch/rewards")
app.include_router(db.router, prefix="/db")

@app.get("/")
async def root():
    logging.info("OAuth callback received: code=super_secret_code")
    return {"message": "Spotify Twitch Bot is running"}
