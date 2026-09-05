from uuid import UUID

from application.ports.release_repository import ReleaseRepositoryPort
from domain.models.release import Release


class GetRelease:
    def __init__(self, repository: ReleaseRepositoryPort) -> None:
        self.repository = repository

    async def execute(self, release_id: UUID) -> Release | None:
        return await self.repository.get_by_id(release_id)