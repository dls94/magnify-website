from uuid import UUID

from application.ports.artist_repository import ArtistRepositoryPort
from domain.models.artist import Artist
from domain.models.user import User


class GetCurrentArtist:
    def __init__(self, repository: ArtistRepositoryPort) -> None:
        self.repository = repository

    async def execute(self, user: User) -> Artist | None:
        if user.artist_id is None:
            return None

        return await self.repository.get_by_id(UUID(str(user.artist_id)))