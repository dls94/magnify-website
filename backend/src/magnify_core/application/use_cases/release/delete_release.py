from uuid import UUID

from magnify_core.application.ports.release_repository import ReleaseRepositoryPort


class DeleteRelease:
    def __init__(self, repository: ReleaseRepositoryPort) -> None:
        self.repository = repository

    async def execute(self, release_id: UUID) -> bool:
        return await self.repository.delete(release_id)