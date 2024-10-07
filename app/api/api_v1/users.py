from fastapi import APIRouter

from api.api_v1.fastapi_users import fastapi_users
from api.dependencies.authentication.backend import authentication_backend
from core.config import settings
from schemas.user import UserRead, UserCreate, UserUpdate

router = APIRouter(
    prefix=settings.api.v1.users,
    tags=["Users"],
)

router.include_router(
    router=fastapi_users.get_users_router(
        UserRead,
        UserUpdate,
    ),
)
