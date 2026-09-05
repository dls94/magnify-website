from datetime import date
from uuid import uuid4
from application.use_cases.release.update_release import UpdateRelease
from domain.models.release import Release, ReleaseType
from tests.fakes.release_repository import InMemoryReleaseRepository


async def test_update_release_updates_release():
    repository = InMemoryReleaseRepository()

    release = Release(
        title="Original Title",
        artist_id=None,
        release_type=ReleaseType.SINGLE,
        release_date=date(2026, 9, 1),
        cover_url=None,
    )

    await repository.save(release)

    use_case = UpdateRelease(repository)

    result = await use_case.execute(
        release.id,
        title="Updated Title",
        release_type=ReleaseType.EP,
        release_date=date(2026, 10, 1),
        cover_url="https://example.com/cover.jpg",
        upc="123456789",
        spotify_url="https://open.spotify.com/album/test",
    )

    assert result is not None
    assert result.title == "Updated Title"
    assert result.release_type == ReleaseType.EP
    assert result.release_date == date(2026, 10, 1)
    assert result.cover_url == "https://example.com/cover.jpg"
    assert result.upc == "123456789"
    assert result.spotify_url == "https://open.spotify.com/album/test"


async def test_update_release_returns_none_when_release_does_not_exist():
    repository = InMemoryReleaseRepository()
    use_case = UpdateRelease(repository)

    result = await use_case.execute(
        release_id=uuid4(),
        title="Updated Title",
    )

    assert result is None