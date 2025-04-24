from fastapi import APIRouter, Depends
from spotipy import Spotify
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
#from backend.services.spotify_service import SpotifyService
from backend.modules.database.database import get_db, get_db_sync
from backend.models.song_request import SongRequest
from datetime import datetime

router = APIRouter()

async def get_db():
    async with Session() as session:
        yield session

@router.post("/song-request")
async def add_song_request(user_id: int, song_name: str, db: AsyncSession = Depends(get_db)):
    song_request = SongRequest(user_id=user_id, song_name=song_name, requested_at=datetime.utcnow())
    db.add(song_request)
    await db.commit()
    return {"message": "Song request added"}

#@router.get("/username")
#async def get_user_name(db: Session = Depends(get_db_sync)):
    #spotify_service = SpotifyService(db)
    #user_name = spotify_service.get_spotify_userName()
    #return {"user_name": user_name}