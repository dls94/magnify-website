from datetime import UTC, datetime

from application.use_cases.event.create_event import CreateEvent
from domain.models.event import EventType
from tests.fakes.event_repository import InMemoryEventRepository


async def test_create_event():
    repository = InMemoryEventRepository()
    use_case = CreateEvent(repository)

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