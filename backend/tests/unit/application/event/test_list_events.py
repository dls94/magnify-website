from datetime import UTC, datetime

from application.use_cases.event.list_events import ListEvents
from domain.models.event import Event, EventType
from tests.fakes.event_repository import InMemoryEventRepository


def make_event(title: str, event_date: datetime) -> Event:
    return Event(
        title=title,
        description="Description",
        event_type=EventType.CONCERT,
        event_date=event_date,
    )


async def test_list_events():
    repository = InMemoryEventRepository()

    event_1 = make_event(
        "Concert 1",
        datetime(2026, 10, 15, 20, 0, tzinfo=UTC),
    )
    event_2 = make_event(
        "Concert 2",
        datetime(2026, 11, 15, 20, 0, tzinfo=UTC),
    )

    await repository.save(event_1)
    await repository.save(event_2)

    use_case = ListEvents(repository)

    result = await use_case.execute()

    assert result == [event_1, event_2]

async def test_list_upcoming_events():
    repository = InMemoryEventRepository()

    past_event = make_event(
        "Concert passé",
        datetime(2026, 1, 15, 20, 0, tzinfo=UTC),
    )
    upcoming_event = make_event(
        "Concert à venir",
        datetime(2026, 12, 15, 20, 0, tzinfo=UTC),
    )

    await repository.save(past_event)
    await repository.save(upcoming_event)

    use_case = ListEvents(repository)

    result = await use_case.execute_upcoming()

    assert result == [upcoming_event]