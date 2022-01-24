from fastapi import Request, Response

from .common import render


async def get_index(request: Request) -> Response:
    return render("index.html", {"request": request})
