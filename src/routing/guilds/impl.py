from fastapi import APIRouter

from src.impl.database import Guild, get_guild, get_guild_config

from .models import CreateGuildRequest, CreateGuildResponse

router = APIRouter(prefix="/guilds", tags=["Guilds"])


@router.post("/", response_model=CreateGuildResponse)
async def create_guild(request: CreateGuildRequest) -> CreateGuildResponse:
    """
    Create a guild in the API.

    This operation will always succeed. If the guild already exists it will be returned.
    """

    guild = await get_guild(request.id, strict=False)

    return CreateGuildResponse(**guild.dict())
