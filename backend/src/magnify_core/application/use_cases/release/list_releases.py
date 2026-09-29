from magnify_core.application.ports.release_repository import ReleaseRepositoryPort
from magnify_core.domain.models import Release


class ListReleases:
    def __init__(self, repository: ReleaseRepositoryPort) -> None:
        self.repository = repository

    async def execute(self) -> list[Release]:
        return await self.repository.list_all()