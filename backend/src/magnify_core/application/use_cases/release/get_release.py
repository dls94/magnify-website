from uuid import UUID

from magnify_core.application.ports.release_repository import ReleaseRepositoryPort
from magnify_core.domain.models import Release


class GetRelease:
    def __init__(self, repository: ReleaseRepositoryPort) -> None:
        self.repository = repository

    async def execute(self, release_id: UUID) -> Release | None:
        return await self.repository.get_by_id(release_id)