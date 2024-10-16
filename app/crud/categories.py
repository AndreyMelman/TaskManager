from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from models import Category, User
from schemas.category import CategoryCreate


async def create_category(
    session: AsyncSession,
    category_in: CategoryCreate,
    user: User,
) -> Category:
    category = Category(name=category_in.name, user=user)
    session.add(category)
    await session.commit()
    await session.refresh(category)
    return category


async def get_categories(
    session: AsyncSession,
    user: User,
) -> list[Category]:
    stmt = select(Category).order_by(Category.id).where(Category.user_id == user.id)
    result: Result = await session.execute(stmt)
    categories = result.scalars().all()
    return list(categories)


async def get_category_by_id(
    session: AsyncSession,
    item_id: int,
    user: User,
):
    stmt = select(Category).where(
        Category.id == item_id,
        Category.user_id == user.id,
    )
    result: Result = await session.execute(stmt)
    category = result.scalars().first()
    return category
