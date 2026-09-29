from datetime import date
from uuid import UUID

from magnify_core.application.exceptions import ArtistNotFoundError
from magnify_core.application.ports.artist_repository import ArtistRepositoryPort
from magnify_core.application.ports.release_repository import ReleaseRepositoryPort
from magnify_core.domain.models import Release, ReleaseType


class CreateRelease:
    def __init__(
        self,
        repository: ReleaseRepositoryPort,
        artist_repository: ArtistRepositoryPort,
    ) -> None:
        self.repository = repository
        self.artist_repository = artist_repository

    async def execute(
        self,
        title: str,
        artist_id: UUID | None,
        release_type: ReleaseType,
        release_date: date,
        cover_url: str | None,
    ) -> Release:
        if artist_id is not None:
            artist = await self.artist_repository.get_by_id(artist_id)

            if artist is None:
                raise ArtistNotFoundError("Artist not found")

        release = Release(
            title=title,
            artist_id=artist_id,
            release_type=release_type,
            release_date=release_date,
            cover_url=cover_url,
        )

        return await self.repository.save(release)