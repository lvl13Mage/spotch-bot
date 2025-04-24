from backend.modules.twitch.twitch_bot_client import TwitchBotClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from backend.modules.twitch.models.reward import Reward
from sqlalchemy.exc import NoResultFound, IntegrityError
from backend.modules.twitch.schemas.reward_type import RewardType
from backend.modules.twitch.schemas.reward import RewardUpdate
from fastapi import APIRouter, Depends, HTTPException
from twitchio.user import PartialUser

class TwitchRewardService:
    def __init__(self, db: AsyncSession, bot: TwitchBotClient):
        self.db = db
        self.bot = bot

    async def create_reward(self, name: str, description: str, amount: int, reward_type: str, active: int = 1) -> Reward:
        """Create a new reward in the database."""
        if reward_type not in [t.value for t in RewardType]:
            raise ValueError(f"Invalid reward type: {reward_type}. Allowed types: {[t.value for t in RewardType]}")

        reward = Reward(name=name, description=description, amount=amount, type=reward_type, active=active)
        self.db.add(reward)
        try:
            await self.db.commit()
            await self.db.refresh(reward)
        except IntegrityError as e:
            await self.db.rollback()
            if "reward_type_check" in str(e.orig):
                raise ValueError(f"Invalid reward type: {reward_type}. Allowed types: {[t.value for t in RewardType]}")
            raise
        return reward

    async def get_rewards(self, active_only: bool = True) -> list[Reward]:
        """Retrieve rewards from the database. Optionally filter by active status."""
        query = select(Reward)
        if active_only:
            query = query.where(Reward.active == 1)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def set_twitch_rewards(self):
        """Sync active rewards to Twitch by creating or updating them."""
        rewards = await self.get_rewards(active_only=False)
        broadcaster = await self.get_broadcaster()

        try:
            # Fetch existing rewards from Twitch
            existing_rewards = await broadcaster.fetch_custom_rewards()
            existing_rewards_map = self._map_rewards_by_id(existing_rewards)
            existing_rewards_by_name = self._map_rewards_by_name(existing_rewards)

            for reward in rewards:
                print(f"Syncing reward: {reward.name} (ID: {reward.id})")
                if reward.twitch_reward_id:
                    reward = await self._sync_reward_by_id(reward, existing_rewards_map, existing_rewards_by_name, broadcaster)
                    print(f"Final Updated Twitch reward ID: {reward.twitch_reward_id}")
                else:
                    reward = await self._sync_or_create_reward_by_name(reward, existing_rewards_by_name, broadcaster)
                # Refresh the reward object in the session
                print(f"Reward ID: {reward.id}, Twitch Reward ID: {reward.twitch_reward_id}")
                await self.db.merge(reward)  # Merge the updated reward back into the session
            # Commit all changes after processing all rewards
            await self.db.commit()
            
            # get the updated rewards from the database
            updated_rewards = await self.get_rewards(active_only=False)
            # Map the updated rewards by their Twitch reward ID
            updated_rewards_map = self._map_rewards_by_id(updated_rewards)
            # Print the updated rewards
            for reward in updated_rewards:
                if reward.twitch_reward_id in updated_rewards_map:
                    print(f"Updated Twitch Reward ID: {reward.twitch_reward_id}")
                else:
                    print(f"Reward ID {reward.id} does not exist in Twitch rewards. Twitch Reward ID: {reward.twitch_reward_id}")
            
        except Exception as e:
            await self.db.rollback()
            raise ValueError(f"Failed to sync rewards to Twitch: {str(e)}")

    def _map_rewards_by_id(self, rewards):
        """Map Twitch rewards by their ID."""
        return {reward.id: reward for reward in rewards}

    def _map_rewards_by_name(self, rewards):
        """Map Twitch rewards by their title (case-insensitive)."""
        return {reward.title.lower(): reward for reward in rewards}

    async def _sync_reward_by_id(self, reward, existing_rewards_map, existing_rewards_by_name, broadcaster):
        """Sync a reward by its Twitch reward ID."""
        if reward.twitch_reward_id in existing_rewards_map:
            print(f"Reward ID {reward.twitch_reward_id} exists in Twitch rewards.")
            # Update the existing reward on Twitch
            twitch_reward = existing_rewards_map[reward.twitch_reward_id]
            await twitch_reward.update(
                title=reward.name,
                cost=reward.amount,
                prompt=reward.description,
                enabled=bool(reward.active)
            )
            return reward
        else:
            print(f"Reward ID {reward.twitch_reward_id} does not exist in Twitch rewards.")
            # Reward ID exists in DB but not on Twitch
            return await self._sync_or_create_reward_by_name(reward, existing_rewards_by_name, broadcaster)

    async def _sync_or_create_reward_by_name(self, reward, existing_rewards_by_name, broadcaster):
        """Sync or create a reward by its name (case-insensitive)."""
        reward_name_lower = reward.name.lower()
        if reward_name_lower in existing_rewards_by_name:
            print(f"Reward name '{reward_name_lower}' exists in Twitch rewards.")
            # Update the existing reward on Twitch by name
            try:
                twitch_reward = existing_rewards_by_name[reward_name_lower]
                await twitch_reward.update(
                    title=reward.name,
                    cost=reward.amount,
                    prompt=reward.description,
                    enabled=bool(reward.active)
                )
                print(f"Twitch Reward ID: {twitch_reward.id}")
                print(f"Current Twitch Reward ID: {reward.twitch_reward_id}")
                reward.twitch_reward_id = twitch_reward.id  # Save the Twitch reward ID to the database
                print(f"Updated Twitch reward ID: {reward.twitch_reward_id}")
                return reward
            except Exception as e:
                raise ValueError(f"Failed to update reward '{reward.name}' on Twitch: {str(e)}")
        else:
            print(f"Reward name '{reward_name_lower}' does not exist in Twitch rewards.")
            # Create a new reward on Twitch
            try:
                print(f"Creating new reward on Twitch: {reward.name}")
                new_reward = await broadcaster.create_custom_reward(
                    title=reward.name,
                    cost=reward.amount,
                    prompt=reward.description,
                    enabled=bool(reward.active)
                )
                reward.twitch_reward_id = new_reward.id  # Save the new Twitch reward ID to the database
                return reward
            except Exception as e:
                raise ValueError(f"Failed to create reward '{reward.name}' on Twitch: {str(e)}")

    async def remove_twitch_rewards(self):
        """Remove active rewards from Twitch."""
        rewards = await self.get_rewards(active_only=False)
        broadcaster = await self.get_broadcaster()
        existing_rewards = await broadcaster.fetch_custom_rewards()
        existing_rewards_map = self._map_rewards_by_id(existing_rewards)
        for reward in rewards:
            print(f"Removing reward: {reward.name} (ID: {reward.id})")
            try:
                # if reward exists in twitch, remove it
                if reward.twitch_reward_id and reward.twitch_reward_id in existing_rewards_map:
                    print(f"Removing reward ID {reward.twitch_reward_id} from Twitch.")
                    # Remove the reward from Twitch
                    await broadcaster.delete_custom_reward(id=reward.twitch_reward_id)
            except Exception as e:
                raise ValueError(f"Failed to remove reward '{reward.name}' from Twitch: {str(e)}")

    async def enable_reward(self, reward_id: int):
        """Enable a reward by setting its active field to 1."""
        reward = await self.get_reward_by_id(reward_id)
        reward.active = 1
        await self.db.commit()

    async def disable_reward(self, reward_id: int):
        """Disable a reward by setting its active field to 0."""
        reward = await self.get_reward_by_id(reward_id)
        reward.active = 0
        await self.db.commit()

    async def get_reward_by_id(self, reward_id: int) -> Reward:
        """Retrieve a specific reward by its ID."""
        try:
            result = await self.db.execute(select(Reward).where(Reward.id == reward_id))
            return result.scalar_one()
        except NoResultFound:
            raise ValueError(f"Reward with ID {reward_id} not found.")

    async def delete_reward(self, reward_id: int):
        """Delete a reward from the database."""
        reward = await self.get_reward_by_id(reward_id)
        await self.db.delete(reward)
        await self.db.commit()

    async def edit_reward(self, reward_id: int, reward_update: RewardUpdate) -> Reward:
        """Edit an existing reward."""
        reward = await self.get_reward_by_id(reward_id)
        if reward_update.name is not None:
            reward.name = reward_update.name
        if reward_update.description is not None:
            reward.description = reward_update.description
        if reward_update.amount is not None:
            reward.amount = reward_update.amount
        if reward_update.type is not None:
            if reward_update.type not in [t.value for t in RewardType]:
                raise ValueError(f"Invalid reward type: {reward_update.type}. Allowed types: {[t.value for t in RewardType]}")
            reward.type = reward_update.type
        if reward_update.active is not None:
            reward.active = reward_update.active

        try:
            await self.db.commit()
            await self.db.refresh(reward)
        except IntegrityError as e:
            await self.db.rollback()
            if "reward_type_check" in str(e.orig):
                raise ValueError(f"Invalid reward type: {reward_update.type}. Allowed types: {[t.value for t in RewardType]}")
            raise
        return reward

    async def get_broadcaster(self) -> PartialUser:
        """Create a PartialUser for the broadcaster."""
        print("Fetching broadcaster details...")
        try:
            bot_channel_name = self.bot.channel_name
            bot_user_id = self.bot.user_id
            return self.bot.create_partialuser(user_id=bot_user_id, user_login=bot_channel_name)
        except Exception as e:
            raise ValueError(f"Failed to create PartialUser for broadcaster: {str(e)}")