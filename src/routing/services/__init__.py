from fastapi import APIRouter

from .cleanleave import router as cleanleave_router
from .todo import router as todo_router

router = APIRouter(prefix="/services")

router.include_router(cleanleave_router)
router.include_router(todo_router)
