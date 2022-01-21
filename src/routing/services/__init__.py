from fastapi import APIRouter

from .todo import router as todo_router

router = APIRouter(prefix="/services")

router.include_router(todo_router)
