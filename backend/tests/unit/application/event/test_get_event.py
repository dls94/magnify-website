from datetime import UTC, datetime

from application.use_cases.event.get_event import GetEvent
from domain.models.event import Event, EventType
from tests.fakes.event_repository import InMemoryEventRepository


async def test_get_event():
    repository = InMemoryEventRepository()

    event = Event(
        title="Concert Magnify",
        description="Un concert Magnify Music.",
        event_type=EventType.CONCERT,
        event_date=datetime(2026, 10, 15, 20, 0, tzinfo=UTC),
    )

    await repository.save(event)

    use_case = GetEvent(repository)

    result = await use_case.execute(event.id)

    assert result is event