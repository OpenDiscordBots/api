from cachingutils import acached
from fastapi import HTTPException
from ormar import JSON, BigInteger, Boolean, ForeignKey, Model, NoMatch, String

from .metadata import database, metadata


class Guild(Model):
    class Meta:
        database = database
        metadata = metadata
        tablename = "guilds"

    # pyright: reportGeneralTypeIssues=false
    id: int = BigInteger(primary_key=True, autoincrement=False)
    banned: bool = Boolean(default=False)


class GuildConfig(Model):
    class Meta:
        database = database
        metadata = metadata
        tablename = "guildconfigs"

    # pyright: reportGeneralTypeIssues=false
    guild: Guild = ForeignKey(Guild, primary_key=True)
    service: str = String(max_length=255, primary_key=True)
    data: dict = JSON()


@acached(timeout=15)
async def get_guild(guild_id: int, strict: bool = False) -> Guild:
    try:
        guild = await Guild.objects.first(id=guild_id)
    except NoMatch:
        guild = await Guild(id=guild_id).save()

    if strict and guild.banned:
        raise HTTPException(400, "Guild is banned.")

    return guild


@acached(timeout=15)
async def get_guild_config(guild_id: int, service: str, strict: bool = False) -> GuildConfig:
    try:
        config = await GuildConfig.objects.first(guild=guild_id, service=service)
    except NoMatch as e:
        guild = await get_guild(guild_id, strict=strict)
        config = await GuildConfig(guild=guild.id, service=service, data={})

    return config
