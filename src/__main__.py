from hmac import compare_digest
from os import environ

from dotenv import load_dotenv
from fastapi import FastAPI, Request, Response

load_dotenv()

from src.impl.database import database

from .routing import router

API_KEY = environ.get("API_KEY")

if not API_KEY:
    raise Exception("API_KEY not set")

app = FastAPI()

app.include_router(router)


@app.on_event("startup")
async def startup() -> None:
    await database.connect()


@app.middleware("http")
async def ensure_auth(request: Request, call_next) -> Response:
    path = request.url.path

    if path.startswith(("/docs", "/openapi.json")):
        return await call_next(request)

    auth = request.headers.get("Authorization")

    if not (auth and compare_digest(auth, API_KEY)):
        return Response(status_code=401)

    return await call_next(request)
