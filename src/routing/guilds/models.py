from pydantic import BaseModel


class CreateGuildRequest(BaseModel):
    id: int


class GuildResponse(CreateGuildRequest):
    banned: bool


class UpdateGuildRequest(BaseModel):
    banned: bool


class GuildConfigRequest(BaseModel):
    data: dict
