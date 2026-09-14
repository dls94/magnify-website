from datetime import UTC, datetime
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from application.exceptions import ArtistNotFoundError
from application.ports.artist_repository import ArtistRepositoryPort
from application.ports.event_repository import EventRepositoryPort
from application.use_cases.event.update_event import UpdateEvent
from domain.models.artist import Artist
from domain.models.event import Event, EventType
from tests.fakes.event_repository import InMemoryEventRepository


async def test_update_event():
    repository = InMemoryEventRepository()
    artist_repository = AsyncMock(spec=ArtistRepositoryPort)

    event = Event(
        title="Concert Magnify",
        description="Description initiale",
        event_type=EventType.CONCERT,
        event_date=datetime(2026, 10, 15, 20, 0, tzinfo=UTC),
    )

    await repository.save(event)

    use_case = UpdateEvent(repository, artist_repository)

    result = await use_case.execute(
        event.id,
        title="Concert Magnify Deluxe",
        description="Nouvelle description",
        city="Paris",
    )

    assert result is not None
    assert result.title == "Concert Magnify Deluxe"
    assert result.description == "Nouvelle description"
    assert result.city == "Paris"
    assert result.event_type == EventType.CONCERT

async def test_update_event_returns_none_when_not_found():
    repository = InMemoryEventRepository()
    artist_repository = AsyncMock(spec=ArtistRepositoryPort)

    use_case = UpdateEvent(repository, artist_repository)

    result = await use_case.execute(
        uuid4(),
        title="Événement inexistant",
    )

    assert result is None

async def test_update_event_rejects_unknown_artist():
    repository = AsyncMock(spec=EventRepositoryPort)
    artist_repository = AsyncMock(spec=ArtistRepositoryPort)

    event = Event(
        title="Test Event",
        description="Description",
        event_type=EventType.CONCERT,
        event_date=datetime.now(UTC),
    )

    repository.get_by_id.return_value = event
    artist_repository.get_by_id.return_value = None

    use_case = UpdateEvent(repository, artist_repository)

    with pytest.raises(ArtistNotFoundError, match="Artist not found"):
        await use_case.execute(
            event_id=event.id,
            artist_id=uuid4(),
            artist_id_provided=True,
        )

    repository.save.assert_not_awaited()

async def test_update_event_can_clear_artist():
    repository = AsyncMock(spec=EventRepositoryPort)
    artist_repository = AsyncMock(spec=ArtistRepositoryPort)

    artist_id = uuid4()

    event = Event(
        title="Test Event",
        description="Description",
        event_type=EventType.CONCERT,
        event_date=datetime.now(UTC),
        artist_id=artist_id,
    )

    repository.get_by_id.return_value = event
    repository.save.return_value = event

    use_case = UpdateEvent(repository, artist_repository)

    result = await use_case.execute(
        event_id=event.id,
        artist_id=None,
        artist_id_provided=True,
    )

    assert result is event
    assert result.artist_id is None
    repository.save.assert_awaited_once()

async def test_update_event_accepts_existing_artist():
    repository = AsyncMock(spec=EventRepositoryPort)
    artist_repository = AsyncMock(spec=ArtistRepositoryPort)

    artist_id = uuid4()

    event = Event(
        title="Test Event",
        description="Description",
        event_type=EventType.CONCERT,
        event_date=datetime.now(UTC),
    )

    artist_repository.get_by_id.return_value = Artist(
        id=artist_id,
        name="Test Artist",
    )
    repository.get_by_id.return_value = event
    repository.save.return_value = event

    use_case = UpdateEvent(repository, artist_repository)

    result = await use_case.execute(
        event_id=event.id,
        artist_id=artist_id,
        artist_id_provided=True,
    )

    assert result.artist_id == artist_id
    artist_repository.get_by_id.assert_awaited_once_with(artist_id)
    repository.save.assert_awaited_once()