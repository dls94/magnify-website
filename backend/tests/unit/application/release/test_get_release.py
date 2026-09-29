from datetime import date
from uuid import uuid4

from magnify_core.application import GetRelease
from magnify_core.domain.models import Release, ReleaseType
from tests.fakes.release_repository import InMemoryReleaseRepository


async def test_get_release_returns_release():
    repository = InMemoryReleaseRepository()

    release = Release(
        id=uuid4(),
        title="Echo Urbain",
        artist_id=None,
        release_type=ReleaseType.SINGLE,
        release_date=date(2026, 9, 1),
        cover_url=None,
    )

    await repository.save(release)

    use_case = GetRelease(repository)

    result = await use_case.execute(release.id)

    assert result is release


async def test_get_release_returns_none_when_release_does_not_exist():
    repository = InMemoryReleaseRepository()
    use_case = GetRelease(repository)

    result = await use_case.execute(uuid4())

    assert result is None