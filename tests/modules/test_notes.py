import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from crud.notes import create_note, get_notes, delete_note
from schemas.note import NoteCreate

from contextlib import nullcontext as does_not_raise

from tests.utils.note import create_random_note
from tests.utils.user import create_random_user


@pytest.mark.asyncio(loop_scope="session")
@pytest.mark.parametrize(
    "title, content, expected",
    [
        ("Test Note1", "Content1", does_not_raise()),
        ("Test Note2", "Content2", does_not_raise()),
        (3, "Content3", pytest.raises(ValueError)),
        ("Test Note4", 4, pytest.raises(ValueError)),
        (5, 5, pytest.raises(ValueError)),
        (None, "Content6", pytest.raises(ValueError)),
        ("Test Note4", None, does_not_raise()),
        ("", "Content8", pytest.raises(ValueError)),
        ("Test Note9", "", does_not_raise()),
        ("Test Note10", True, pytest.raises(ValueError)),
        (False, "Content11", pytest.raises(ValueError)),
        (
            "111111111111111111111111111111111111111111111111111",
            "Content12",
            pytest.raises(ValueError),
        ),
    ],
)
async def test_create_note(
    session: AsyncSession,
    title: str,
    content: str,
    expected,
):
    user = await create_random_user(session=session)
    with expected:
        note_data = NoteCreate(
            title=title,
            content=content,
        )
        new_note = await create_note(session=session, note_in=note_data, user=user)

        assert new_note.title == title
        assert new_note.content == content
        assert new_note.user == user


@pytest.mark.asyncio(loop_scope="session")
async def test_get_notes(
    session: AsyncSession,
):
    user = await create_random_user(session=session)
    note = await create_random_note(session=session, superuser=user)
    session.add(note)
    await session.commit()

    notes = await get_notes(
        session=session,
        user=user,
    )

    assert len(notes) == len(notes)
    assert notes == list(notes)
    assert notes is not None

    for note in notes:
        assert note.user_id == user.id


@pytest.mark.asyncio(loop_scope="session")
async def test_get_notes_no_notes(
    session: AsyncSession,
):
    user = await create_random_user(session=session)
    notes = await get_notes(
        session=session,
        user=user,
    )

    assert notes == []


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_note(
    session: AsyncSession,
):
    user = await create_random_user(session=session)
    note = await create_random_note(session=session, superuser=user)
    session.add(note)
    await session.commit()
    del_note = await session.delete(note)

    assert del_note is None
