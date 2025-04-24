from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from backend.modules.database.database import get_db
from backend.modules.twitch.services.twitch_reward_service import TwitchRewardService
from backend.modules.twitch.schemas.reward import RewardCreate, RewardResponse, RewardUpdate
from typing import List

router = APIRouter()

def get_twitch_reward_service(
    db: AsyncSession = Depends(get_db),
    request: Request = None  # Inject the request to access the bot
) -> TwitchRewardService:
    print("Creating TwitchRewardService")
    bot = request.app.state.twitch_bot  # Access the bot from app state
    return TwitchRewardService(db=db, bot=bot)

@router.post("/create", response_model=RewardResponse)
async def create_reward(
    reward: RewardCreate,
    service: TwitchRewardService = Depends(get_twitch_reward_service)
):
    """Create a new reward in the database."""
    try:
        created_reward = await service.create_reward(
            name=reward.name,
            description=reward.description,
            amount=reward.amount,
            reward_type=reward.type,
            active=reward.active
        )
        return created_reward
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail="Database integrity error occurred.")

@router.get("/list", response_model=List[RewardResponse])
async def list_rewards(
    active_only: bool = True,
    service: TwitchRewardService = Depends(get_twitch_reward_service)
):
    """List all rewards, optionally filtering by active status."""
    rewards = await service.get_rewards(active_only=active_only)
    return rewards

@router.put("/{reward_id}/edit", response_model=RewardResponse)
async def edit_reward(
    reward_id: int,
    reward_update: RewardUpdate,
    service: TwitchRewardService = Depends(get_twitch_reward_service)
):
    """Edit an existing reward."""
    try:
        updated_reward = await service.edit_reward(reward_id, reward_update)
        return updated_reward
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail="Database integrity error occurred.")

@router.post("/{reward_id}/activate")
async def activate_reward(
    reward_id: int,
    service: TwitchRewardService = Depends(get_twitch_reward_service)
):
    """Activate a reward by setting its active field to 1 in the database."""
    try:
        await service.enable_reward(reward_id)
        return {"status": "Reward activated in the database. Sync to apply changes to Twitch."}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/{reward_id}/deactivate")
async def deactivate_reward(
    reward_id: int,
    service: TwitchRewardService = Depends(get_twitch_reward_service)
):
    """Deactivate a reward by setting its active field to 0 in the database."""
    try:
        await service.disable_reward(reward_id)
        return {"status": "Reward deactivated in the database. Sync to apply changes to Twitch."}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{reward_id}/delete")
async def delete_reward(
    reward_id: int,
    service: TwitchRewardService = Depends(get_twitch_reward_service)
):
    """Delete a reward from the database."""
    try:
        await service.delete_reward(reward_id)
        return {"status": "Reward deleted"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/sync")
async def sync_rewards_to_twitch(
    service: TwitchRewardService = Depends(get_twitch_reward_service)
):
    """Sync active rewards to Twitch by creating or updating them as channel point rewards."""
    try:
        await service.set_twitch_rewards()
        return {"status": "Twitch rewards synced"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/remove")
async def remove_rewards_from_twitch(
    service: TwitchRewardService = Depends(get_twitch_reward_service)
):
    """Remove active rewards from Twitch."""
    try:
        await service.remove_twitch_rewards()
        return {"status": "Twitch rewards removed"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))