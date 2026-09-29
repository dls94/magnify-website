from magnify_core.application.ports.release_repository import ReleaseRepositoryPort
from magnify_core.domain.models import Release, User


class GetCurrentArtistReleases:
    def __init__(self, repository: ReleaseRepositoryPort) -> None:
        self.repository = repository

    async def execute(self, user: User) -> list[Release]:
        if user.artist_id is None:
            return []

        return await self.repository.list_by_artist_id(user.artist_id)