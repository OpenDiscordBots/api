from hmac import compare_digest
from os import environ

from dotenv import load_dotenv
from fastapi import FastAPI, Request, Response
from fastapi.staticfiles import StaticFiles

load_dotenv()

from src.impl.auth import Authenticator
from src.impl.database import database

from .routing import router
from .ui import router as ui_router

API_KEY = environ.get("API_KEY")

if not API_KEY:
    raise Exception("API_KEY not set")

authenticator = Authenticator()

app = FastAPI()

app.mount("/static", StaticFiles(directory="./src/ui/static"), name="static")

app.include_router(router)
app.include_router(ui_router)


@app.on_event("startup")
async def startup() -> None:
    await database.connect()


@app.middleware("http")
async def ensure_auth(request: Request, call_next) -> Response:
    path = request.url.path

    if path.startswith(("/docs", "/openapi.json", "/oauth", "/static")):
        request.state.oauth = authenticator

        return await call_next(request)

    if path.startswith("/ui"):
        user = await authenticator.get_auth(request)

        if not user:
            return authenticator.oauth.redirect()

        request.state.user = user
        return await call_next(request)

    auth = request.headers.get("Authorization")

    if not (auth and compare_digest(auth, API_KEY)):
        return Response(status_code=401)

    return await call_next(request)
