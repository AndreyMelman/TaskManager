from fastapi import APIRouter

from core.config import settings
from .notes import router as notes_router
from .tasks import router as tasks_router

router = APIRouter(prefix=settings.api.v1.prefix)

router.include_router(notes_router, prefix=settings.api.v1.notes)
router.include_router(tasks_router, prefix=settings.api.v1.tasks)