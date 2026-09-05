from datetime import UTC, datetime, timedelta
from uuid import uuid4

from domain.models.event import Event, EventType
from infrastructure.database.connection import AsyncSessionLocal
from infrastructure.database.repositories.event_repository import EventRepository


async def test_save_persists_event():
    event = Event(
        title="Concert Magnify",
        description="Un concert Magnify Music.",
        event_type=EventType.CONCERT,
        event_date=datetime(2026, 10, 15, 20, 0, tzinfo=UTC),
        venue_name="La Cigale",
        city="Paris",
        ticket_url="https://example.com/tickets",
    )

    async with AsyncSessionLocal() as session:
        repository = EventRepository(session)
        saved_event = await repository.save(event)

    assert saved_event is event


async def test_get_by_id_returns_event():
    event = Event(
        title="Release Party",
        description="Présentation du nouvel album.",
        event_type=EventType.RELEASE_PARTY,
        event_date=datetime(2026, 11, 20, 20, 0, tzinfo=UTC),
        city="Paris",
    )

    async with AsyncSessionLocal() as session:
        repository = EventRepository(session)
        await repository.save(event)

        retrieved_event = await repository.get_by_id(event.id)

    assert retrieved_event is not None
    assert retrieved_event.id == event.id
    assert retrieved_event.title == event.title
    assert retrieved_event.description == event.description
    assert retrieved_event.event_type == EventType.RELEASE_PARTY
    assert retrieved_event.event_date == event.event_date
    assert retrieved_event.city == event.city


async def test_get_by_id_returns_none_when_event_does_not_exist():
    async with AsyncSessionLocal() as session:
        repository = EventRepository(session)

        event = await repository.get_by_id(
            uuid4(),
        )

    assert event is None


async def test_list_all_returns_events():
    first_event = Event(
        title="Concert 1",
        description="Premier concert.",
        event_type=EventType.CONCERT,
        event_date=datetime(2026, 10, 10, 20, 0, tzinfo=UTC),
    )
    second_event = Event(
        title="Festival 1",
        description="Premier festival.",
        event_type=EventType.FESTIVAL,
        event_date=datetime(2026, 10, 20, 18, 0, tzinfo=UTC),
    )

    async with AsyncSessionLocal() as session:
        repository = EventRepository(session)
        await repository.save(first_event)
        await repository.save(second_event)

        events = await repository.list_all()

    event_ids = {event.id for event in events}

    assert first_event.id in event_ids
    assert second_event.id in event_ids


async def test_list_upcoming_returns_only_future_events():
    past_event = Event(
        title="Ancien concert",
        description="Un concert passé.",
        event_type=EventType.CONCERT,
        event_date=datetime.now(UTC) - timedelta(days=1),
    )
    future_event = Event(
        title="Prochain concert",
        description="Un concert à venir.",
        event_type=EventType.CONCERT,
        event_date=datetime.now(UTC) + timedelta(days=10),
    )

    async with AsyncSessionLocal() as session:
        repository = EventRepository(session)
        await repository.save(past_event)
        await repository.save(future_event)

        events = await repository.list_upcoming()

    event_ids = {event.id for event in events}

    assert past_event.id not in event_ids
    assert future_event.id in event_ids


async def test_save_updates_existing_event():
    event = Event(
        title="Concert Magnify",
        description="Description initiale.",
        event_type=EventType.CONCERT,
        event_date=datetime(2026, 10, 15, 20, 0, tzinfo=UTC),
    )

    async with AsyncSessionLocal() as session:
        repository = EventRepository(session)
        await repository.save(event)

        event.update_profile(
            title="Concert Magnify Updated",
            description="Nouvelle description.",
            city="Paris",
        )
        await repository.save(event)

        retrieved_event = await repository.get_by_id(event.id)

    assert retrieved_event is not None
    assert retrieved_event.title == "Concert Magnify Updated"
    assert retrieved_event.description == "Nouvelle description."
    assert retrieved_event.city == "Paris"


async def test_delete_removes_event():
    event = Event(
        title="Concert à supprimer",
        description="Événement temporaire.",
        event_type=EventType.CONCERT,
        event_date=datetime(2026, 12, 1, 20, 0, tzinfo=UTC),
    )

    async with AsyncSessionLocal() as session:
        repository = EventRepository(session)
        await repository.save(event)

        deleted = await repository.delete(event.id)
        retrieved_event = await repository.get_by_id(event.id)

    assert deleted is True
    assert retrieved_event is None


async def test_delete_returns_false_when_event_does_not_exist():
    async with AsyncSessionLocal() as session:
        repository = EventRepository(session)

        deleted = await repository.delete(
            uuid4(),
        )

    assert deleted is False