import asyncio
import aiohttp
import logging
import json
from sqlalchemy.ext.asyncio import AsyncSession
from backend.modules.auth.services.twitch_auth_service import TwitchAuthService
from backend.modules.twitch.services.twitch_eventsub_service import TwitchEventSubService
from backend.modules.twitch.services.twitch_chat_service import TwitchChatService
from backend.modules.twitch.twitch_bot_client import TwitchBotClient

TWITCH_EVENTSUB_WS_URL = "wss://eventsub.wss.twitch.tv/ws"
TWITCH_API_SUBSCRIPTIONS = "https://api.twitch.tv/helix/eventsub/subscriptions"

class TwitchEventSubWebSocketHandler:
    def __init__(self, db, client_id: str, access_token: str, user_id: str):
        self.db = db
        self.client_id = client_id
        self.access_token = access_token
        self.user_id = user_id
        self.session_id = None
        self.keepalive_timeout = 10 * 60  # default fallback
        self.ws_task = None
        self._running = True
        self._ws_session = None  # Save the session for graceful closing
        
    @classmethod
    async def create(cls, db: AsyncSession) -> "TwitchEventSubWebSocketHandler":
        twitch_auth_service = TwitchAuthService(db)
        credentials = await twitch_auth_service.get_twitch_credentials()
        return cls(db, credentials.client_id, credentials.twitch_token.access_token, credentials.twitch_token.user_id)

    async def start(self):
        while self._running:
            try:
                async with aiohttp.ClientSession() as session:
                    self._ws_session = session
                    async with session.ws_connect(TWITCH_EVENTSUB_WS_URL) as ws:
                        async for msg in ws:
                            if not self._running:
                                break
                            if msg.type == aiohttp.WSMsgType.TEXT:
                                await self._handle_message(session, msg.json())
                            elif msg.type == aiohttp.WSMsgType.ERROR:
                                logging.warning("WebSocket error: %s", msg.data)
                                break
            except Exception as e:
                if not self._running:
                    break
                logging.error(f"WebSocket connection failed: {e}")

            if not self._running:
                break

            logging.info("Cleaning up old subscriptions...")
            await self._unsubscribe_all()
            logging.info("Reconnecting to Twitch EventSub WebSocket in 5 seconds...")
            await asyncio.sleep(5)

    async def stop(self):
        logging.info("🛑 Stopping EventSub WebSocket handler...")
        self._running = False
        await self._unsubscribe_all()
        if self._ws_session:
            await self._ws_session.close()

    async def _handle_message(self, session, data):
        metadata = data.get("metadata", {})
        msg_type = metadata.get("message_type")

        if msg_type == "session_welcome":
            self.session_id = data["payload"]["session"]["id"]
            logging.info(f"Connected to Twitch EventSub WebSocket")
            await self._register_subscriptions(session)

        elif msg_type == "notification":
            event_type = data["payload"]["subscription"]["type"]
            event_data = data["payload"]["event"]
            await self._dispatch_event(event_type, event_data)

        elif msg_type == "session_keepalive":
            logging.debug("Received keepalive")

        elif msg_type == "session_reconnect":
            new_url = data["payload"]["session"]["reconnect_url"]
            logging.warning(f"Twitch requested reconnect to: {new_url}")
            # optional: implement reconnect handling here

    async def _register_subscriptions(self, session):
        headers = {
            "Client-ID": self.client_id,
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        body = {
            "type": "channel.channel_points_custom_reward_redemption.add",
            "version": "1",
            "condition": {"broadcaster_user_id": self.user_id},
            "transport": {
                "method": "websocket",
                "session_id": self.session_id
            }
        }        
        async with session.post(TWITCH_API_SUBSCRIPTIONS, headers=headers, data=json.dumps(body)) as resp:
            if resp.status == 202:
                logging.info("Successfully subscribed to channel point redemptions.")
            else:
                error = await resp.text()
                logging.error(f"Failed to register subscription: {resp.status}, {error}")

    async def _unsubscribe_all(self):
        headers = {
            "Client-ID": self.client_id,
            "Authorization": f"Bearer {self.access_token}"
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(TWITCH_API_SUBSCRIPTIONS, headers=headers) as resp:
                if resp.status != 200:
                    logging.error(f"Failed to fetch subscriptions: {resp.status}")
                    return
                data = await resp.json()
                for sub in data.get("data", []):
                    sub_id = sub.get("id")
                    if sub_id:
                        async with session.delete(f"{TWITCH_API_SUBSCRIPTIONS}?id={sub_id}", headers=headers) as del_resp:
                            if del_resp.status == 204:
                                logging.info(f"Unsubscribed from {sub.get('type')} ({sub_id})")
                            else:
                                logging.warning(f"Failed to unsubscribe {sub_id}: {del_resp.status}")

    async def _dispatch_event(self, event_type: str, event: dict):
        if event_type == "channel.channel_points_custom_reward_redemption.add":
            bot = await TwitchBotClient.create(self.db)
            twitch_chat_service = TwitchChatService(bot)
            service = TwitchEventSubService(self.db, twitch_chat_service)
            await service.handle_redemption(event)
        else:
            logging.warning(f"Unhandled EventSub event type: {event_type}")
