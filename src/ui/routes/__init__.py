from fastapi import APIRouter

from .index import get_index

router = APIRouter(prefix="/ui", include_in_schema=False)

router.get("")(get_index)
