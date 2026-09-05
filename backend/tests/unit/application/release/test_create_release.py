from datetime import date

from domain.models.release import ReleaseType
from tests.fakes.release_repository import InMemoryReleaseRepository
from application.use_cases.release.create_release import CreateRelease


async def test_create_release_saves_release():
    repository = InMemoryReleaseRepository()
    use_case = CreateRelease(repository)

    release = await use_case.execute(
        title="Echo Urbain",
        artist_id=None,
        release_type=ReleaseType.SINGLE,
        release_date=date(2026, 9, 1),
        cover_url=None,
    )

    assert release.title == "Echo Urbain"
    assert release.release_type == ReleaseType.SINGLE
    assert release.release_date == date(2026, 9, 1)
    assert repository.releases[release.id] is release