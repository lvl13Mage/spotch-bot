from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from sqlalchemy.future import select
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
def set_spotify_credentials(data: SpotifyCredentialInput, db: Session = Depends(get_db_sync)):
    """Set or update API credentials for a service (Spotify)."""
    spotify_auth_service = SpotifyAuthService(db)
    spotify_auth_service.set_credentials(data)
    return {"message": "Spotify credentials updated successfully!"}

@router.get("/spotify/credentials")
def get_spotify_credentials(db: Session = Depends(get_db_sync)):
    """Fetch Spotify credentials from the database."""
    spotify_auth_service = SpotifyAuthService(db)
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
        return {"clientId": "", "clientSecret": ""}
    return credentials