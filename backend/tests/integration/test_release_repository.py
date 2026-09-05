from datetime import date

from domain.models.release import Release, ReleaseType
from infrastructure.database.connection import AsyncSessionLocal
from infrastructure.database.repositories.release_repository import ReleaseRepository


async def test_save_persists_release_with_tracks():
    release = Release(
        title="Echo Urbain",
        release_type=ReleaseType.SINGLE,
        release_date=date(2026, 9, 1),
        cover_url="https://example.com/cover.jpg",
    )

    release.add_track(
        title="Intro",
        duration_seconds=120,
        isrc="FR-TEST-00001",
    )
    release.add_track(
        title="Echo Urbain",
        duration_seconds=210,
        isrc="FR-TEST-00002",
    )

    async with AsyncSessionLocal() as session:
        repository = ReleaseRepository(session)

        saved_release = await repository.save(release)

    assert saved_release is release


async def test_get_by_id_reconstructs_release_with_tracks():
    release = Release(
        title="Echo Urbain",
        release_type=ReleaseType.SINGLE,
        release_date=date(2026, 9, 1),
        cover_url="https://example.com/cover.jpg",
    )

    release.add_track("Intro", 120, "FR-TEST-00001")
    release.add_track("Echo Urbain", 210, "FR-TEST-00002")

    async with AsyncSessionLocal() as session:
        repository = ReleaseRepository(session)

        await repository.save(release)

    async with AsyncSessionLocal() as session:
        repository = ReleaseRepository(session)

        result = await repository.get_by_id(release.id)

    assert result is not None
    assert result.id == release.id
    assert result.title == "Echo Urbain"
    assert result.release_type == ReleaseType.SINGLE
    assert result.release_date == date(2026, 9, 1)
    assert result.cover_url == "https://example.com/cover.jpg"

    assert len(result.tracks) == 2

    assert result.tracks[0].title == "Intro"
    assert result.tracks[0].track_number == 1
    assert result.tracks[0].duration_seconds == 120
    assert result.tracks[0].isrc == "FR-TEST-00001"

    assert result.tracks[1].title == "Echo Urbain"
    assert result.tracks[1].track_number == 2
    assert result.tracks[1].duration_seconds == 210
    assert result.tracks[1].isrc == "FR-TEST-00002"

async def test_save_updates_existing_release_and_tracks():
    release = Release(
        title="Echo Urbain",
        release_type=ReleaseType.SINGLE,
        release_date=date(2026, 9, 1),
        cover_url="https://example.com/cover.jpg",
    )
    release.add_track("Intro", 120, "FR-TEST-00001")

    async with AsyncSessionLocal() as session:
        repository = ReleaseRepository(session)
        await repository.save(release)

    release.title = "Echo Urbain - Deluxe"
    release.tracks.clear()
    release.add_track("Nouveau morceau", 180, "FR-TEST-00003")

    async with AsyncSessionLocal() as session:
        repository = ReleaseRepository(session)
        await repository.save(release)

    async with AsyncSessionLocal() as session:
        repository = ReleaseRepository(session)
        result = await repository.get_by_id(release.id)

    assert result is not None
    assert result.title == "Echo Urbain - Deluxe"
    assert len(result.tracks) == 1
    assert result.tracks[0].title == "Nouveau morceau"
    assert result.tracks[0].track_number == 1
    assert result.tracks[0].isrc == "FR-TEST-00003"

async def test_delete_release_cascades_to_tracks():
    release = Release(
        title="Echo Urbain",
        release_type=ReleaseType.SINGLE,
        release_date=date(2026, 9, 1),
        cover_url="https://example.com/cover.jpg",
    )
    release.add_track("Intro", 120, "FR-TEST-00001")
    release.add_track("Echo Urbain", 210, "FR-TEST-00002")

    async with AsyncSessionLocal() as session:
        repository = ReleaseRepository(session)
        await repository.save(release)

    async with AsyncSessionLocal() as session:
        repository = ReleaseRepository(session)

        deleted = await repository.delete(release.id)

        assert deleted is True

    async with AsyncSessionLocal() as session:
        repository = ReleaseRepository(session)

        result = await repository.get_by_id(release.id)

        assert result is None