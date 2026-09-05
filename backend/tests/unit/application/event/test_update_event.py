from datetime import UTC, datetime
from uuid import uuid4

from application.use_cases.event.update_event import UpdateEvent
from domain.models.event import Event, EventType
from tests.fakes.event_repository import InMemoryEventRepository


async def test_update_event():
    repository = InMemoryEventRepository()

    event = Event(
        title="Concert Magnify",
        description="Description initiale",
        event_type=EventType.CONCERT,
        event_date=datetime(2026, 10, 15, 20, 0, tzinfo=UTC),
    )

    await repository.save(event)

    use_case = UpdateEvent(repository)

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
    use_case = UpdateEvent(repository)

    result = await use_case.execute(
        uuid4(),
        title="Événement inexistant",
    )

    assert result is None