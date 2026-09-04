from uuid import UUID

from application.ports.artist_repository import ArtistRepositoryPort


class DeleteArtist:
    def __init__(self, repository: ArtistRepositoryPort) -> None:
        self.repository = repository

    async def execute(self, artist_id: UUID) -> bool:
        return await self.repository.delete(artist_id)