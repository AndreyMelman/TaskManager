from fastapi import HTTPException, status
from sqlalchemy import select, Result

from sqlalchemy.ext.asyncio import AsyncSession

from models import Profile, User
from schemas.profile import ProfileCreate, ProfileUpdate


async def create_user_profile(
    session: AsyncSession,
    user: User,
    profile_in: ProfileCreate,
) -> Profile:
    stmt = select(Profile).where(Profile.user_id == user.id)
    result = await session.execute(stmt)
    profile_ex = result.scalars().first()

    if profile_ex:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, detail="Profile already exists for this user"
        )
    profile = Profile(**profile_in.model_dump(), user_id=user.id)
    session.add(profile)
    await session.commit()
    return profile


async def get_profile(
    session: AsyncSession,
    user: User,
) -> Profile | None:
    stmt = select(Profile).where(Profile.user_id == user.id)
    result: Result = await session.execute(stmt)
    profile = result.scalar()
    if profile is not None:
        return profile
    raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Profile not found")


async def update_user_profile(
    session: AsyncSession,
    profile_update: ProfileUpdate,
    user: User,
    partial: bool = False,
) -> Profile:
    profile = await session.execute(select(Profile).where(Profile.user_id == user.id))
    profile = profile.scalars().first()
    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")

    for name, value in profile_update.model_dump(exclude_unset=partial).items():
        setattr(profile, name, value)
    await session.commit()
    return profile
