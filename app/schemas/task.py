from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TaskBase(BaseModel):
    title: str
    description: str
    priority: str
    deadline_at: datetime
    completed: bool


class CreateNote(TaskBase):
    pass


class UpdateTask(TaskBase):
    pass


class UpdateTaskPartial(TaskBase):
    title: str | None = None
    description: str | None = None
    priority: str | None = None
    deadline_at: datetime | None = None
    completed: bool | None = None


class Task(TaskBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
