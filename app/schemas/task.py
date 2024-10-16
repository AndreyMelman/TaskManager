from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from models.task import PriorityEnum


class TaskBase(BaseModel):
    title: str = Field(default="", min_length=1, max_length=50)
    description: str = Field(default="", max_length=50000)
    priority: PriorityEnum = PriorityEnum.low
    deadline_at: datetime = Field(default=datetime.now())
    completed: bool = Field(default=False)


class TaskCreate(TaskBase):
    pass


class TaskUpdate(TaskCreate):
    title: str | None = Field(default=None, min_length=1, max_length=50)
    description: str | None = Field(default=None, max_length=50000)
    priority: PriorityEnum | None = None
    deadline_at: datetime | None = Field(default=datetime.now())
    completed: bool | None = Field(default=False)


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
