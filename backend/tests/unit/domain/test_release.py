import pytest
from datetime import date, datetime, timezone
from uuid import UUID
from domain.models.release import Release, ReleaseType, Track

ARTIST_ID = UUID("12345678-1234-5678-1234-567812345678")

def make_release(**kwargs) -> Release:
    defaults = {
        "title": "Echo Urbain",
        "artist_id": ARTIST_ID,
        "release_type": ReleaseType.SINGLE,
        "release_date": date(2026, 9, 1),
    }
    defaults.update(kwargs)
    return Release(**defaults)

def test_release_can_be_created_without_tracks():
    release = make_release()

    assert release.title == "Echo Urbain"
    assert release.tracks == []
    assert release.is_published is False

def test_add_track_adds_track_number_one():
    release = make_release()

    release.add_track(
        title="Intro",
        duration_seconds=180,
    )

    assert len(release.tracks) == 1
    assert release.tracks[0].title == "Intro"
    assert release.tracks[0].track_number == 1

def test_add_track_increments_track_number():
    release = make_release()

    release.add_track("Intro", 120)
    release.add_track("Echo Urbain", 210)
    release.add_track("Outro", 150)

    assert [track.track_number for track in release.tracks] == [1, 2, 3]

def test_release_cannot_be_published_without_tracks():
    release = make_release(
        cover_url="https://example.com/cover.jpg"
    )

    assert release.can_be_published() is False

def test_release_cannot_be_published_without_cover():
    release = make_release()

    release.add_track("Echo Urbain", 210)

    assert release.can_be_published() is False

def test_release_can_be_published_with_cover_and_track():
    release = make_release(
        cover_url="https://example.com/cover.jpg"
    )

    release.add_track("Echo Urbain", 210)

    assert release.can_be_published() is True

def test_publish_publishes_valid_release():
    release = make_release(
        cover_url="https://example.com/cover.jpg"
    )
    release.add_track("Echo Urbain", 210)

    release.publish()

    assert release.is_published is True

def test_publish_rejects_invalid_release():
    release = make_release()

    with pytest.raises(ValueError, match="Impossible de publier"):
        release.publish()

    assert release.is_published is False

def test_track_requires_a_title():
    with pytest.raises(ValueError):
        Track(
            title="",
            duration_seconds=180,
        )

def test_track_rejects_blank_title():
    with pytest.raises(ValueError):
        Track(
            title="   ",
            duration_seconds=180,
        )

def test_track_requires_positive_duration():
    with pytest.raises(ValueError):
        Track(
            title="Echo Urbain",
            duration_seconds=0,
        )

def test_track_rejects_negative_duration():
    with pytest.raises(ValueError):
        Track(
            title="Echo Urbain",
            duration_seconds=-10,
        )

def test_cannot_publish_release_twice():
    release = make_release(
        cover_url="https://example.com/cover.jpg"
    )
    release.add_track("Echo Urbain", 210)

    release.publish()

    with pytest.raises(ValueError, match="déjà publiée"):
        release.publish()

def test_track_rejects_invalid_track_number():
    with pytest.raises(ValueError):
        Track(
            title="Echo Urbain",
            duration_seconds=210,
            track_number=0,
        )


def test_release_has_timezone_aware_creation_date():
    release = make_release()

    assert isinstance(release.created_at, datetime)
    assert release.created_at.tzinfo == timezone.utc