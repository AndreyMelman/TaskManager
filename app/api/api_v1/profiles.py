from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import db_helper
from crud import profiles
from api.api_v1.fastapi_users import current_active_user
from core.config import settings
from models import User
from schemas.profile import ProfileCreate, Profile, ProfileUpdate

router = APIRouter(
    prefix=settings.api.v1.profiles,
    tags=["Profiles"],
)


@router.post(
    "/",
    response_model=Profile,
    status_code=status.HTTP_201_CREATED,
)
async def create_user_profile(
    profile_in: ProfileCreate,
    session: AsyncSession = Depends(db_helper.getter_session),
    user: User = Depends(current_active_user),
):
    return await profiles.create_user_profile(
        session=session,
        user=user,
        profile_in=profile_in,
    )


@router.get("/", response_model=Profile)
async def get_user_profile(
    session: AsyncSession = Depends(db_helper.getter_session),
    user: User = Depends(current_active_user),
):
    return await profiles.get_profile(
        session=session,
        user=user,
    )


@router.patch("/", response_model=Profile)
async def update_user_profile(
    profile_update: ProfileUpdate,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(db_helper.getter_session),
):
    return await profiles.update_user_profile(
        session=session,
        profile_update=profile_update,
        user=user,
        partial=True,
    )
