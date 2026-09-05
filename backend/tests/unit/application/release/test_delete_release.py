from datetime import date
from uuid import uuid4

from application.use_cases.release.delete_release import DeleteRelease
from domain.models.release import Release, ReleaseType
from tests.fakes.release_repository import InMemoryReleaseRepository


async def test_delete_release_deletes_release():
    repository = InMemoryReleaseRepository()

    release = Release(
        title="Echo Urbain",
        artist_id=None,
        release_type=ReleaseType.SINGLE,
        release_date=date(2026, 9, 1),
        cover_url=None,
    )

    await repository.save(release)

    use_case = DeleteRelease(repository)

    result = await use_case.execute(release.id)

    assert result is True
    assert release.id not in repository.releases


async def test_delete_release_returns_false_when_release_does_not_exist():
    repository = InMemoryReleaseRepository()
    use_case = DeleteRelease(repository)

    result = await use_case.execute(uuid4())

    assert result is False