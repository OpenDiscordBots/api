from ormar import BigInteger, Model, String

from .metadata import database, metadata


class JoinMessage(Model):
    class Meta:
        database = database
        metadata = metadata
        tablename = "joinmessages"

    # pyright: reportGeneralTypeIssues=false
    id_slug: str = String(max_length=255, primary_key=True)  # workaround for composite pkey
    channel_id: int = BigInteger()
    message_id: int = BigInteger()
