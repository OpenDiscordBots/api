from ormar import BigInteger, Boolean, ForeignKey, Model, String

from .metadata import database, metadata
from .user import User


class Todo(Model):
    class Meta:
        database = database
        metadata = metadata
        tablename = "todos"

    # pyright: reportGeneralTypeIssues=false
    id: int = BigInteger(primary_key=True)
    user: User = ForeignKey(User)
    task: str = String(max_length=512)
    done: bool = Boolean(default=False)
    namespace: str = String(max_length=255, default="default")
