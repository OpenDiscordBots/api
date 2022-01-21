from fastapi import APIRouter

from .services import router as service_router

router = APIRouter()

router.include_router(service_router)
