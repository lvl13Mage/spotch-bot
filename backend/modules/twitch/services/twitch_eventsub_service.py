from backend.modules.twitch.schemas.reward_type import RewardType
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from backend.modules.twitch.models.reward import Reward
from backend.modules.spotify.services.song_request_service import SongRequestService
from backend.modules.twitch.services.twitch_chat_service import TwitchChatService

class TwitchEventSubService:
    def __init__(self, db, twitch_chat_service):
        self.db = db
        self.twitch_chat_service = twitch_chat_service
        
    async def get_rewards(self, active_only: bool = True) -> list[Reward]:
        """Retrieve rewards from the database. Optionally filter by active status."""
        query = select(Reward)
        if active_only:
            query = query.where(Reward.active == 1)
        result = await self.db.execute(query)
        return result.scalars().all()


    async def handle_redemption(self, event: dict):
        print(f"🎁 Redemption: {event['reward']['title']} by {event['user_name']}")
        # Route to reward-specific logic here if needed
        # switch case for rewartd title
        
        # get rewards from db
        rewards = await self.get_rewards(active_only=True)
        # check rewardm title and get corresponding reward type
        print(f"Debug event: {event}")
        for reward in rewards:
            if reward.name == event['reward']['title']:
                print(f"Reward found: {reward.name}")            
                match reward.type:
                    case RewardType.SONG_QUEUE_ADD.technical_label:
                        print(f"Adding song to queue: {event['user_input']}")
                        spotify_song_request_service = SongRequestService()
                        songsearch = spotify_song_request_service.search_song(event['user_input'])
                        if songsearch:
                            print(f"Song found: {songsearch[0]['artists']} - {songsearch[0]['name']}")
                            spotify_song_request_service.add_song_to_song_queue(song_id=songsearch[0]['id'])
                            await self.twitch_chat_service.send_message(f"Added to queue: {songsearch[0]['artists']} - {songsearch[0]['name']}")
                        else:
                            print(f"Song not found: {event['user_input']}")

    async def handle_stream_online(self, event: dict):
        print(f"🟢 Stream is now online for {event['broadcaster_user_id']}")

    async def handle_stream_offline(self, event: dict):
        print(f"🔴 Stream is now offline for {event['broadcaster_user_id']}")
