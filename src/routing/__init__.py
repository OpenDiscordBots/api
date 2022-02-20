from fastapi import APIRouter

from .guilds import router as guilds_router
from .services import router as service_router

router = APIRouter(prefix="/api")

router.include_router(guilds_router)
router.include_router(service_router)
