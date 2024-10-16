from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.fastapi_users import current_active_user
from api.dependencies.load_by_id import category_getter
from core.db import db_helper
from models import User
from schemas.category import Category, CategoryCreate
from crud import categories

router = APIRouter(
    tags=["Categories"],
)


@router.get("/", response_model=list[Category])
async def get_categories(
    session: AsyncSession = Depends(db_helper.getter_session),
    user: User = Depends(current_active_user),
):
    return await categories.get_categories(
        session=session,
        user=user,
    )


@router.get("/{category_id}", response_model=Category)
async def get_category(
    category: Category = Depends(category_getter),
):
    return category


@router.post("/", response_model=Category)
async def create_category(
    category_in: CategoryCreate,
    session: AsyncSession = Depends(db_helper.getter_session),
    user: User = Depends(current_active_user),
):
    return await categories.create_category(
        session=session,
        category_in=category_in,
        user=user,
    )