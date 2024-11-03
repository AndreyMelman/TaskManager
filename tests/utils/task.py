from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from crud.tasks import create_task
from models import User, Task
from models.task import PriorityEnum
from schemas.task import TaskCreate

from tests.utils.utils import random_lower_string


async def create_random_task(session: AsyncSession, superuser: User) -> Task:
    title = await random_lower_string()
    description = await random_lower_string()
    priority = PriorityEnum.low
    deadline_at = datetime.now()
    completed = False
    task_in = TaskCreate(
        title=title,
        description=description,
        priority=priority,
        deadline_at=deadline_at,
        completed=completed,
    )
    return await create_task(session=session, task_in=task_in, user=superuser)
