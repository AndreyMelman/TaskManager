from pydantic import BaseModel, ConfigDict, Field


class CategoryBase(BaseModel):
    name: str = Field(min_length=1, max_length=32, description="Category name")


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(CategoryCreate):
    name: str | None = Field(default=None, max_length=32)


class Category(CategoryBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
