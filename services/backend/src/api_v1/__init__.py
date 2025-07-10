from fastapi import APIRouter

from .user.views import router as user_router


router = APIRouter(prefix="/v1")


router.include_router(user_router, prefix='/users')