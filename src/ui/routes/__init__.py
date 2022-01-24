from fastapi import APIRouter

from .index import get_index

router = APIRouter(prefix="/ui")

router.get("")(get_index)
