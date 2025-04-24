from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from backend.modules.database.database import get_db, get_db_sync
from backend.modules.twitch.twitch_bot_client import TwitchBotClient
from backend.modules.auth.services.twitch_auth_service import TwitchAuthService
from backend.modules.twitch.services.twitch_chat_service import TwitchChatService
import logging

router = APIRouter()

@router.get("/message")
async def send_message(request: Request):
    bot = request.app.state.twitch_bot
    
    chat = TwitchChatService(bot)
    await chat.send_message("Persistent Twitch bot says hi!")
    return {"status": "Message sent"}
    