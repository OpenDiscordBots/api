from pydantic import BaseModel


class CreateGuildRequest(BaseModel):
    id: int


class GuildResponse(CreateGuildRequest):
    banned: bool
