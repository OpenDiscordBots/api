from fastapi import APIRouter, Request, Response
from fastapi.responses import RedirectResponse

router = APIRouter(prefix="/oauth")


@router.get("/callback")
async def callback(request: Request, code: str) -> Response | RedirectResponse:
    auth = await request.state.oauth.login(code)

    if not auth:
        return Response(status_code=401, content="Invalid authentication")

    resp = RedirectResponse(url="/ui")
    resp.set_cookie("__odb_token", auth)

    return resp
