from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
import logging
from backend.modules.database.database import get_db, get_db_sync
from backend.modules.auth.services.twitch_auth_service import TwitchAuthService
from backend.modules.auth.schemas.twitch_credential import TwitchCredentialInput
from backend.modules.auth.schemas.spotify_credential import SpotifyCredentialInput
from backend.modules.auth.services.spotify_auth_service import SpotifyAuthService

router = APIRouter()

@router.post("/twitch/set")
async def set_credentials(data: TwitchCredentialInput, db: AsyncSession = Depends(get_db)):
    """Set or update API credentials for a service (Twitch)."""
    twitch_auth_service = TwitchAuthService(db)
    await twitch_auth_service.set_credentials(data)
    return {"message": "Twitch credentials updated successfully!"}
    

@router.post("/spotify/set")
def set_spotify_credentials(request: Request, data: SpotifyCredentialInput, db: Session = Depends(get_db_sync)):
    """Set or update API credentials for a service (Spotify)."""
    spotify_auth_service = SpotifyAuthService(db, request.app)
    spotify_auth_service.set_credentials(data)
    return {"message": "Spotify credentials updated successfully!"}

@router.get("/spotify/credentials")
def get_spotify_credentials(request: Request, db: Session = Depends(get_db_sync)):
    """Fetch Spotify credentials from the database."""
    spotify_auth_service = SpotifyAuthService(db, request.app)
    credentials = spotify_auth_service.get_credentials()
    if not credentials:
        return {"clientId": "", "clientSecret": ""}
    return credentials

@router.get("/twitch/credentials")
async def get_twitch_credentials(db: AsyncSession = Depends(get_db)):
    """Fetch Twitch credentials from the database."""
    twitch_auth_service = TwitchAuthService(db)
    credentials = await twitch_auth_service.get_credentials()
    if not credentials:
        return {"client_id": "", "client_secret": "", "scope": "", "redirect_uri": ""}
    return credentials


@router.get("/status/twitch")
async def twitch_credentials_status(db: AsyncSession = Depends(get_db)):
    """Check if Twitch credentials are set."""
    service = TwitchAuthService(db)
    credentials = await service.get_twitch_credentials()
    return {"twitch_credentials_set": bool(credentials)}

@router.get("/status/spotify")
def spotify_credentials_status(request: Request, db: Session = Depends(get_db_sync)):
    """Check if Spotify credentials are set."""
    service = SpotifyAuthService(db, request.app)
    credentials = service.get_credentials()
    return {"spotify_credentials_set": bool(credentials)}

@router.delete("/spotify/delete")
def delete_spotify_credentials(request: Request, db: Session = Depends(get_db_sync)):
    """Delete Spotify credentials and token using the service."""
    spotify_auth_service = SpotifyAuthService(db, request.app)
    spotify_auth_service.delete_credentials_and_token()
    return {"message": "Spotify credentials and token deleted successfully."}

@router.delete("/twitch/delete")
async def delete_twitch_credentials(db: AsyncSession = Depends(get_db)):
    """Delete Twitch credentials and token using the service."""
    twitch_auth_service = TwitchAuthService(db)
    try:
        await twitch_auth_service.delete_credentials_and_token()
        return {"message": "Twitch credentials and token deleted successfully."}
    except Exception as e:
        logging.error(f"Error deleting Twitch credentials: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to delete Twitch credentials.")