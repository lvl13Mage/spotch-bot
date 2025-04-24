from twitchio.ext.commands import Bot
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

class TwitchBotClient(Bot):

    def __init__(
        self,
        token: str,
        client_id: str,
        initial_channels: list[str],
        user_id: str,
        bot_id: str,
        db: AsyncSession,
        credential: TwitchCredential,
        twitch_token: TwitchToken,
    ):
        self.db = db
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
    async def create(cls, db: AsyncSession) -> "TwitchBotClient":
        service = TwitchAuthService(db)
        credential = await service.get_twitch_credentials()
        token_obj = credential.twitch_token

        return cls(
            token=token_obj.access_token.replace("oauth:", ""),
            client_id=credential.client_id,
            initial_channels=[token_obj.channel_name],
            user_id=token_obj.user_id,
            bot_id=token_obj.user_id,
            db=db,
            credential=credential,
            twitch_token=token_obj,
        )
        
    async def load_tokens(self):
        """(Optional) Reload tokens from DB, e.g., after refresh."""
        service = TwitchAuthService(self.db)
        credential = await service.get_twitch_credentials()
        token_obj = credential.twitch_token

        await self.add_token(token_obj.access_token.replace("oauth:", ""), token_obj.refresh_token)

    async def event_ready(self):
        print(f"✅ Logged in as {self.user.name}")
        self._ready_event.set()

    async def wait_until_ready(self):
        await self._ready_event.wait()
        print("✅ Bot is ready.")

    async def start_bot(self):
        print("🚀 Starting bot...")
        await self.start()
        print("��� Bot started.")

    async def stop_bot(self):
        await self.close()

    # --- Handlers ---

    async def event_channel_points_custom_reward_redemption_add(self, data: dict, db: AsyncSession):
        handler = TwitchEventSubService(db)
        await handler.handle_redemption(data)

    async def event_stream_online(self, data: dict):
        handler = TwitchEventSubService(self.db)
        await handler.handle_stream_online(data)

    async def event_stream_offline(self, data: dict):
        handler = TwitchEventSubService(self.db)
        await handler.handle_stream_offline(data)
