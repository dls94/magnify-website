from uuid import UUID

from magnify_core.application.ports.artist_repository import ArtistRepositoryPort
from magnify_core.domain.models import Artist


class GetArtist:

    def __init__(self, repository: ArtistRepositoryPort) -> None:
        self.repository = repository

    async def execute(self, artist_id: UUID) -> Artist | None:
        return await self.repository.get_by_id(artist_id)