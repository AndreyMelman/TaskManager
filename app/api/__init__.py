from fastapi import APIRouter
from .api_v1.notes import router as notes_router
from .api_v1.tasks import router as tasks_router


router = APIRouter()

router.include_router(notes_router, prefix="/notes")
router.include_router(tasks_router, prefix="/tasks")