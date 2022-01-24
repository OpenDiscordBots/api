from dataclasses import dataclass
from json import dumps, loads
from os import environ
from secrets import token_hex

from aioredis import Redis, from_url
from fastapi import Request
from starlette_discord import DiscordOAuthClient, User


@dataclass
class Authentication:
    user_id: int
    username: str
    discriminator: str
    avatar: str


class Authenticator:
    def __init__(self) -> None:
        self.oauth = DiscordOAuthClient(
            client_id=environ["CLIENT_ID"],
            client_secret=environ["CLIENT_SECRET"],
            redirect_uri=environ["URL_BASE"] + "/api/oauth/callback",
        )
        self.redis: Redis = from_url(environ["REDIS_URI"])
        self.owners = [int(owner) for owner in environ["OWNERS"].split(",")]

    async def get_auth(self, request: Request) -> Authentication | None:
        token = request.cookies.get("__odb_token")

        if not token:
            return

        data = await self.redis.get(token)
        if not data:
            return

        # Refresh the token to be valid for another 7 days
        await self.redis.set(token, data, ex=86400 * 7)

        data = loads(data)

        return Authentication(**data)

    async def create_auth(self, user: User) -> str | None:
        if user.id not in self.owners:
            return

        token = token_hex(64)

        data = {
            "user_id": user.id,
            "username": user.username,
            "discriminator": user.discriminator,
            "avatar": user.avatar,
        }

        await self.redis.set(token, dumps(data), ex=86400 * 7)

        return token

    async def login(self, code: str) -> str | None:
        token = await self.create_auth(await self.oauth.login(code))

        return token
