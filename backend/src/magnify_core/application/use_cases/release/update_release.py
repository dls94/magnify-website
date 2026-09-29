from datetime import date
from uuid import UUID

from magnify_core.application.exceptions import ArtistNotFoundError
from magnify_core.application.ports.artist_repository import ArtistRepositoryPort
from magnify_core.application.ports.release_repository import ReleaseRepositoryPort
from magnify_core.domain.models import Release, ReleaseType


class UpdateRelease:
    def __init__(
        self,
        repository: ReleaseRepositoryPort,
        artist_repository: ArtistRepositoryPort,
    ) -> None:
        self.repository = repository
        self.artist_repository = artist_repository

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
        artist_id_provided: bool = False,
    ) -> Release | None:
        release = await self.repository.get_by_id(release_id)

        if release is None:
            return None

        if artist_id_provided and artist_id is not None:
            artist = await self.artist_repository.get_by_id(artist_id)

            if artist is None:
                raise ArtistNotFoundError("Artist not found")

        release.update_profile(
            title=title,
            release_type=release_type,
            release_date=release_date,
            cover_url=cover_url,
            upc=upc,
            spotify_url=spotify_url,
            artist_id=artist_id,
            artist_id_provided=artist_id_provided,
        )

        return await self.repository.save(release)