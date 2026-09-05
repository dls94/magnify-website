from datetime import date

from application.use_cases.release.list_releases import ListReleases
from domain.models.release import Release, ReleaseType
from tests.fakes.release_repository import InMemoryReleaseRepository


async def test_list_releases_returns_all_releases():
    repository = InMemoryReleaseRepository()

    release_one = Release(
        title="Echo Urbain",
        artist_id=None,
        release_type=ReleaseType.SINGLE,
        release_date=date(2026, 9, 1),
        cover_url=None,
    )
    release_two = Release(
        title="Nuit Blanche",
        artist_id=None,
        release_type=ReleaseType.EP,
        release_date=date(2026, 10, 1),
        cover_url=None,
    )

    await repository.save(release_one)
    await repository.save(release_two)

    use_case = ListReleases(repository)

    result = await use_case.execute()

    assert result == [release_one, release_two]


async def test_list_releases_returns_empty_list_when_no_release_exists():
    repository = InMemoryReleaseRepository()
    use_case = ListReleases(repository)

    result = await use_case.execute()

    assert result == []