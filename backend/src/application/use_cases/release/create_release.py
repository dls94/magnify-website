from datetime import date
from uuid import UUID

from application.ports.release_repository import ReleaseRepositoryPort
from domain.models.release import Release
from domain.models.release import ReleaseType


class CreateRelease:
    def __init__(self, repository: ReleaseRepositoryPort) -> None:
        self.repository = repository

    async def execute(
        self,
        title: str,
        artist_id: UUID | None,
        release_type: ReleaseType,
        release_date: date,
        cover_url: str | None,
    ) -> Release:
        release = Release(
            title=title,
            artist_id=artist_id,
            release_type=release_type,
            release_date=release_date,
            cover_url=cover_url,
        )

        return await self.repository.save(release)