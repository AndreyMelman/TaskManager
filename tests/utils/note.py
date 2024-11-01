from sqlalchemy.ext.asyncio import AsyncSession

from crud.notes import create_note
from models import Note, User
from schemas.note import NoteCreate

from tests.utils.utils import random_lower_string


async def create_random_note(session: AsyncSession, superuser: User) -> Note:
    title = await random_lower_string()
    content = await random_lower_string()
    note_in = NoteCreate(title=title, content=content)
    return await create_note(session=session, note_in=note_in, user=superuser)
