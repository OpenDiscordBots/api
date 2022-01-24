from pydantic import BaseModel


class JoinMessageModel(BaseModel):
    channel_id: int
    message_id: int
