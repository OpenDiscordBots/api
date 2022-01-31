from fastapi import APIRouter, HTTPException
from ormar import NoMatch

from src.impl.database import JoinMessage

from .models import JoinMessageModel

router = APIRouter(prefix="/cleanleave")


@router.post("/guilds/{guild_id}/members/{member_id}", status_code=201)
async def create_join_message(request: JoinMessageModel, guild_id: int, member_id: int) -> None:
    """Create a new join message."""

    try:
        join_message = await JoinMessage.objects.first(id_slug=f"{guild_id}:{member_id}")
    except NoMatch:
        await JoinMessage(id_slug=f"{guild_id}:{member_id}", **request.dict()).save()
        return

    await join_message.update(**request.dict())


@router.get("/guilds/{guild_id}/members/{member_id}", response_model=JoinMessageModel)
async def get_join_message(guild_id: int, member_id: int) -> JoinMessageModel:
    """Get a join message."""

    try:
        join_message = await JoinMessage.objects.first(id_slug=f"{guild_id}:{member_id}")
    except NoMatch:
        raise HTTPException(404, "Join message not found")

    return JoinMessageModel(**join_message.dict())


@router.delete("/guilds/{guild_id}/members/{member_id}")
async def delete_join_message(guild_id: int, member_id: int) -> None:
    """
    Delete a join message.

    This operation will always succeed.
    """

    await JoinMessage.objects.delete(id_slug=f"{guild_id}:{member_id}")
