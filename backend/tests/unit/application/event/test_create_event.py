from datetime import UTC, datetime
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from application.exceptions import ArtistNotFoundError
from application.ports.artist_repository import ArtistRepositoryPort
from application.ports.event_repository import EventRepositoryPort
from application.use_cases.event.create_event import CreateEvent
from domain.models.artist import Artist
from domain.models.event import Event, EventType
from tests.fakes.event_repository import InMemoryEventRepository


async def test_create_event():
    repository = InMemoryEventRepository()
    artist_repository = AsyncMock(spec=ArtistRepositoryPort)

    use_case = CreateEvent(repository, artist_repository)

    event = await use_case.execute(
        title="Concert Magnify",
        description="Un concert Magnify Music.",
        event_type=EventType.CONCERT,
        event_date=datetime(2026, 10, 15, 20, 0, tzinfo=UTC),
    )

    assert event.title == "Concert Magnify"
    assert event.description == "Un concert Magnify Music."
    assert event.event_type == EventType.CONCERT
    assert event.is_published is False
    assert event.id in repository.events

async def test_create_event_rejects_unknown_artist():
    repository = AsyncMock(spec=EventRepositoryPort)
    artist_repository = AsyncMock(spec=ArtistRepositoryPort)

    artist_repository.get_by_id.return_value = None

    use_case = CreateEvent(repository, artist_repository)

    with pytest.raises(ArtistNotFoundError, match="Artist not found"):
        await use_case.execute(
            title="Test Event",
            description="Description",
            event_type=EventType.CONCERT,
            event_date=datetime.now(UTC),
            artist_id=uuid4(),
        )

    repository.save.assert_not_awaited()

async def test_create_event_accepts_existing_artist():
    repository = AsyncMock(spec=EventRepositoryPort)
    artist_repository = AsyncMock(spec=ArtistRepositoryPort)

    artist_id = uuid4()

    artist_repository.get_by_id.return_value = Artist(
        id=artist_id,
        name="Test Artist",
    )

    event = Event(
        title="Test Event",
        description="Description",
        event_type=EventType.CONCERT,
        event_date=datetime.now(UTC),
        artist_id=artist_id,
    )
    repository.save.return_value = event

    use_case = CreateEvent(repository, artist_repository)

    result = await use_case.execute(
        title="Test Event",
        description="Description",
        event_type=EventType.CONCERT,
        event_date=event.event_date,
        artist_id=artist_id,
    )

    assert result is event
    assert result.artist_id == artist_id
    artist_repository.get_by_id.assert_awaited_once_with(artist_id)
    repository.save.assert_awaited_once()