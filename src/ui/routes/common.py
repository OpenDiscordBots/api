from fastapi import Response
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="src/ui/templates")


def render(page: str, context: dict) -> Response:
    context["user"] = context["request"].state.user
    return templates.TemplateResponse(page, context)
