import pytest
from datetime import datetime, timezone

from domain.models.event import Event, EventType


def make_event(**kwargs) -> Event:
    defaults = {
        "title": "Concert Magnify",
        "description": "Un concert Magnify Music.",
        "event_type": EventType.CONCERT,
        "event_date": datetime(2026, 10, 15, 20, 0, tzinfo=timezone.utc),
    }
    defaults.update(kwargs)
    return Event(**defaults)


def test_event_can_be_created():
    event = make_event()

    assert event.title == "Concert Magnify"
    assert event.event_type == EventType.CONCERT
    assert event.is_published is False


def test_event_requires_a_title():
    with pytest.raises(ValueError):
        make_event(title="")


def test_event_rejects_blank_title():
    with pytest.raises(ValueError):
        make_event(title="   ")


def test_event_has_timezone_aware_creation_date():
    event = make_event()

    assert isinstance(event.created_at, datetime)
    assert event.created_at.tzinfo == timezone.utc


def test_event_can_be_past():
    event = make_event(
        event_date=datetime(2026, 1, 1, 20, 0, tzinfo=timezone.utc)
    )

    assert event.is_past() is True


def test_event_can_be_future():
    event = make_event(
        event_date=datetime(2026, 12, 1, 20, 0, tzinfo=timezone.utc)
    )

    assert event.is_past() is False


def test_event_can_be_published():
    event = make_event()

    event.publish()

    assert event.is_published is True


def test_event_cannot_be_published_twice():
    event = make_event()

    event.publish()

    with pytest.raises(ValueError, match="déjà publié"):
        event.publish()