from fastapi import APIRouter

from src.impl.database import Guild, GuildConfig
from src.impl.database import get_guild as get_db_guild
from src.impl.database import get_guild_config

from .models import CreateGuildRequest, GuildConfigRequest, GuildResponse

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


@router.post("/{guild_id}/config/{service}", response_model=GuildConfig)
async def create_service_config(guild_id: int, service: str, request: GuildConfigRequest) -> GuildConfig:
    """
    Create a service config in the API.

    This operation will always succeed unless the guild is banned. \
        If the config already exists it will be overwritten.
    """

    config = await get_guild_config(guild_id, service, strict=True)
    config = await config.update(data=request.data)

    return config


@router.get("/{guild_id}/config/{service}", response_model=GuildConfig)
async def get_service_config(guild_id: int, service: str) -> GuildConfig:
    """
    Get a service config from the API.

    This operation will always succeed unless the guild is banned. \
        If the config does not exist an empty config will be created.
    """

    config = await get_guild_config(guild_id, service, strict=False)

    return config


@router.patch("/{guild_id}/config/{service}", response_model=GuildConfig)
async def update_service_config(guild_id: int, service: str, request: GuildConfigRequest) -> GuildConfig:
    """
    Update a service config in the API.

    This operation will always succeed unless the guild is banned. \
        If the config does not exist it will be created.
    """

    config = await get_guild_config(guild_id, service, strict=False)
    config = await config.update(data=request.data)

    return config


@router.delete("/{guild_id}/config/{service}")
async def delete_service_config(guild_id: int, service: str) -> None:
    """
    Delete a service config from the API.

    This operation will always succeed.
    """

    await GuildConfig.objects.delete(guild=guild_id, service=service)
