from twitchio.ext.commands import Bot
from twitchio.ext import commands
from twitchio import eventsub, ChatMessage
from twitchio.eventsub import (
    ChannelPointsRedeemAddSubscription,
    StreamOnlineSubscription,
    StreamOfflineSubscription,
    SubscriptionPayload
)
import asyncio
from backend.modules.auth.models.twitch_credential import TwitchCredential
from backend.modules.auth.models.twitch_token import TwitchToken
from sqlalchemy.ext.asyncio import AsyncSession
from backend.modules.auth.services.twitch_auth_service import TwitchAuthService
from backend.modules.twitch.services.twitch_eventsub_service import TwitchEventSubService
from backend.modules.twitch.services.twitch_chat_service import TwitchChatService
from backend.modules.twitch.components.reward_commands_component import RewardCommandsComponent
from typing import Optional
import logging
from fastapi import FastAPI

class TwitchBotClient(Bot):

    def __init__(
        self,
        token: str,
        client_id: str,
        initial_channels: list[str],
        user_id: str,
        bot_id: str,
        db: AsyncSession,
        app: FastAPI,
        credential: TwitchCredential,
        twitch_token: TwitchToken,
    ):
        self.db = db
        self.app = app
        self.client_id = client_id
        self.user_id = user_id
        self.channel_name = initial_channels[0]
        self.initial_channels = initial_channels

        self._credential = credential
        self._twitch_token = twitch_token

        super().__init__(
            token=token,
            prefix="!",
            initial_channels=initial_channels,
            client_id=client_id,
            bot_id=user_id,
            client_secret=self._credential.client_secret
        )
        print(f"Starting bot with user ID: {self.user_id}")
        self._ready_event = asyncio.Event()
        
        # Define your EventSub subscriptions here
        self.subscriptions: list[SubscriptionPayload] = [
            ChannelPointsRedeemAddSubscription(broadcaster_user_id=self._twitch_token.channel_name),
            StreamOnlineSubscription(broadcaster_user_id=self.user_id),
            StreamOfflineSubscription(broadcaster_user_id=self.user_id)
            # Add more here
        ]
        

    @classmethod
    async def create(cls, db: AsyncSession, app: FastAPI) -> Optional["TwitchBotClient"]:
        service = TwitchAuthService(db)
        credential = await service.get_twitch_credentials()

        if not credential or not credential.twitch_token:
            logging.warning("No Twitch credentials found. Twitch bot will not start.")
            return None  # Return None if credentials are missing

        token_obj = credential.twitch_token

        return cls(
            token=token_obj.access_token.replace("oauth:", ""),
            client_id=credential.client_id,
            initial_channels=[token_obj.channel_name],
            user_id=token_obj.user_id,
            bot_id=token_obj.user_id,
            db=db,
            app=app,
            credential=credential,
            twitch_token=token_obj,
                    )
    
    async def setup_hook(self) -> None:
        logging.info("Setting up Twitch bot...")
        logging.info("Initial Channels: %s", self.initial_channels)
        subscription = eventsub.ChatMessageSubscription(
            broadcaster_user_id=self.user_id,
            user_id=self.user_id
        )
        await self.subscribe_websocket(payload=subscription)
        logging.info("Subscribed to chat messages.")
        await self.load_module(name="backend.modules.twitch.components.reward_commands_component")
        logging.info("Twitch bot setup complete.")
    
    async def load_tokens(self):
        """(Optional) Reload tokens from DB, e.g., after refresh."""
        service = TwitchAuthService(self.db)
        credential = await service.get_twitch_credentials()
        token_obj = credential.twitch_token

        await self.add_token(token_obj.access_token.replace("oauth:", ""), token_obj.refresh_token)

    async def event_ready(self):
        logging.info("Twitch bot is ready.")
        logging.info("Connected to Twitch as %s", self.user_id)
        self._ready_event.set()
    
    # TODO: needs to be removed to avoid infinite loop
    async def event_message(self, payload: ChatMessage) -> None:
        #if payload.chatter.id == self.bot_id:
        #    logging.info("Ignoring message from bot itself.")
        #    return

        if payload.source_broadcaster is not None:
            logging.info("Payload source broadcaster: %s", payload.source_broadcaster)
            return
        
        await self.process_commands(payload)
        
    
    async def wait_until_ready(self):
        await self._ready_event.wait()
        print("✅ Bot is ready.")

    async def start_bot(self):
        print("🚀 Starting bot...")
        await self.start()

    async def stop_bot(self):
        await self.close()

    # --- Handlers ---

    async def event_channel_points_custom_reward_redemption_add(self, data: dict, db: AsyncSession):
        twitch_chat_service = TwitchChatService(self)
        handler = TwitchEventSubService(db, twitch_chat_service, self.app)
        await handler.handle_redemption(data)

    async def event_stream_online(self, data: dict):
        twitch_chat_service = TwitchChatService(self)
        handler = TwitchEventSubService(self.db, twitch_chat_service, self.app)
        await handler.handle_stream_online(data)

    async def event_stream_offline(self, data: dict):
        twitch_chat_service = TwitchChatService(self)
        handler = TwitchEventSubService(self.db, twitch_chat_service, self.app)
        await handler.handle_stream_offline(data)