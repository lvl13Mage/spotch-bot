from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from backend.modules.database.database import get_db, get_db_sync
from backend.modules.auth.services.twitch_auth_service import TwitchAuthService
from backend.modules.auth.services.spotify_auth_service import SpotifyAuthService
from backend.modules.routing.utils.lifecycle import shutdown_tasks, startup_tasks
import logging

router = APIRouter()

@router.get("/twitch")
async def twitch_auth(db: AsyncSession = Depends(get_db)):
    """Returns Twitch OAuth authorization URL"""
    twitch_service = TwitchAuthService(db)
    auth_url = await twitch_service.get_auth_url()
    return {"auth_url": auth_url}

@router.get("/twitch/callback")
async def twitch_callback(code: str, request: Request, db: AsyncSession = Depends(get_db)):
    """Handles Twitch OAuth callback and restarts the app lifecycle."""
    twitch_service = TwitchAuthService(db)
    try:
        # Exchange the code for a token
        token = await twitch_service.get_token_with_code(code)

        # Restart the app lifecycle
        app = request.app  # Access the FastAPI app instance
        logging.info("🔄 Restarting application lifecycle after Twitch callback...")
        await shutdown_tasks(app)  # Call shutdown_tasks from routing/__init__.py
        await startup_tasks(app)  # Call startup_tasks from routing/__init__.py
        logging.info("✅ Application lifecycle restarted successfully.")

        return {"message": "Access token received and application restarted successfully!"}
    except Exception as e:
        logging.error(f"Error exchanging code for token or restarting app: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/twitch/refresh-token")
async def verify_and_refresh_token(db: AsyncSession = Depends(get_db)):
    """Verifies the Twitch token and refreshes it if needed."""
    twitch_service = TwitchAuthService(db)
    try:
        token = await twitch_service.get_valid_token()  # ✅ Get the stored token
        if not token:
            return {"message": "Could not find stored token. Please authorize Twitch first."}
        return {"message": "Token verified and refreshed successfully!"}
    except Exception as e:
        logging.error(f"Error verifying or refreshing Twitch token: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/spotify/authorize")
def spotify_auth(db: Session = Depends(get_db_sync)):
    """Returns Spotify OAuth authorization URL"""
    spotify_auth_service = SpotifyAuthService(db)
    response = spotify_auth_service.spotify_auth_flow()
    
    return response

@router.get("/spotify/callback")
async def spotify_callback(code: str, db: Session = Depends(get_db_sync)):
    if not code:
        return {"message": "No code provided in the request."}
    spotify_auth_service = SpotifyAuthService(db)
    response = spotify_auth_service.get_access_token(code)
    return response
