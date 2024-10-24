from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field


class CategoryBase(BaseModel):
    name: Annotated[str, Field(min_length=1, max_length=255,description="Category name")] = 'Category'



class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(CategoryCreate):
    pass


class Category(CategoryBase):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int
    user_id: int
