from fastapi import APIRouter

from core.config import settings
from schemas.user import UserRead

router = APIRouter(
    prefix=settings.api.v1.auth,
    tags=["Auth"]
)