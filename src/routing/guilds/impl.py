from fastapi import APIRouter

from src.impl.database import Guild, get_guild as get_db_guild, get_guild_config

from .models import CreateGuildRequest, GuildResponse

router = APIRouter(prefix="/guilds", tags=["Guilds"])


@router.post("/", response_model=GuildResponse)
async def create_guild(request: CreateGuildRequest) -> GuildResponse:
    """
    Create a guild in the API.

    This operation will always succeed. If the guild already exists it will be returned.
    """

    guild = await get_db_guild(request.id, strict=False)

    return GuildResponse(**guild.dict())


@router.get("/{guild_id}", response_model=GuildResponse)
async def get_guild(guild_id: int) -> GuildResponse:
    """
    Get a guild from the API.

    This operation will always succeed. If the guild does not exist it will be created.
    """

    guild = await get_db_guild(guild_id, strict=False)

    return GuildResponse(**guild.dict())


@router.patch("/{guild_id}", response_model=GuildResponse)
async def update_guild(guild_id: int, request: CreateGuildRequest) -> GuildResponse:
    """
    Update a guild in the API.

    This operation will always succeed. If the guild does not exist it will be created.
    """

    guild = await get_db_guild(guild_id, strict=False)
    guild = await guild.update(**request.dict())

    return GuildResponse(**guild.dict())


@router.delete("/{guild_id}")
async def delete_guild(guild_id: int) -> None:
    """
    Delete a guild from the API.

    This operation will always succeed.
    """

    await Guild.objects.delete(id=guild_id)
