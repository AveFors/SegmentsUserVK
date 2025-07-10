from fastapi import APIRouter

from .user.views import router as user_router
from .segment.views import router as segment_router


router = APIRouter(prefix="/v1")


router.include_router(user_router, prefix='/users')
router.include_router(segment_router, prefix='/segments')