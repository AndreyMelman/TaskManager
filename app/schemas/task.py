from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class TaskBase(BaseModel):
    title: str
    description: str
    priority: str
    deadline_at: datetime
    completed: bool = Field(default=False)


class TaskCreate(TaskBase):
    pass


class TaskUpdate(TaskCreate):
    title: str | None = None
    description: str | None = None
    priority: str | None = None
    deadline_at: datetime | None = None
    completed: bool | None = None


class Task(TaskBase):
    model_config = ConfigDict(from_attributes=True)

    created_at: datetime
    updated_at: datetime
    id: int
