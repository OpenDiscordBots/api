from fastapi import HTTPException
from ormar import BigInteger, Boolean, Model, NoMatch

from .metadata import database, metadata


class User(Model):
    class Meta:
        database = database
        metadata = metadata
        tablename = "users"

    # pyright: reportGeneralTypeIssues=false
    id: int = BigInteger(primary_key=True, autoincrement=False)
    banned: bool = Boolean(default=False)


async def get_user(user_id: int, strict: bool = False) -> User:
    try:
        user = await User.objects.first(id=user_id)
    except NoMatch:
        user = await User(id=user_id).save()

    if strict and user.banned:
        raise HTTPException(400, "User is banned.")

    return user
