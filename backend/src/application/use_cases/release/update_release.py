from datetime import date
from uuid import UUID

from application.ports.release_repository import ReleaseRepositoryPort
from domain.models.release import Release, ReleaseType


class UpdateRelease:
    def __init__(self, repository: ReleaseRepositoryPort) -> None:
        self.repository = repository

    async def execute(
        self,
        release_id: UUID,
        title: str | None = None,
        release_type: ReleaseType | None = None,
        release_date: date | None = None,
        cover_url: str | None = None,
        upc: str | None = None,
        spotify_url: str | None = None,
        artist_id: UUID | None = None,
    ) -> Release | None:
        release = await self.repository.get_by_id(release_id)

        if release is None:
            return None

        release.update_profile(
            title=title,
            release_type=release_type,
            release_date=release_date,
            cover_url=cover_url,
            upc=upc,
            spotify_url=spotify_url,
            artist_id=artist_id,
        )

        return await self.repository.save(release)