from pydantic import BaseModel


class CreateGuildRequest(BaseModel):
    id: int


class CreateGuildResponse(CreateGuildRequest):
    banned: bool
