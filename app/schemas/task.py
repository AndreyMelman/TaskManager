from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

from models.task import PriorityEnum


class TaskBase(BaseModel):
    title: Annotated[str, Field(min_length=1, max_length=50)] = "title"
    description:Annotated[str | None, Field(max_length=50)] = "description"
    priority: PriorityEnum = Field(default=PriorityEnum.low)
    deadline_at: datetime | None = Field(default=datetime.now())
    completed: bool = Field(default=False)
    category_id: int | None = None

class TaskCreate(TaskBase):
    pass


class TaskUpdate(TaskCreate):
    title: Annotated[str | None, Field(min_length=1, max_length=50)] = None
    description: Annotated[str | None, Field(max_length=50)] = None
    priority: PriorityEnum | None = None
    deadline_at: datetime | None = Field(default=datetime.now())
    completed: bool | None = Field(default=False)
    category_id: int | None = None

class TaskUpdateStatus(BaseModel):
    completed: bool = Field(default=True)


class TaskUpdatePriority(BaseModel):
    priority: PriorityEnum


class Task(TaskBase):
    model_config = ConfigDict(from_attributes=True)

    created_at: datetime
    updated_at: datetime
    id: int
    user_id: int
