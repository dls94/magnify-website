from uuid import UUID

from magnify_core.application.ports.event_repository import EventRepositoryPort
from magnify_core.domain.models import Event


class GetEvent:
    def __init__(self, repository: EventRepositoryPort) -> None:
        self.repository = repository

    async def execute(self, event_id: UUID) -> Event | None:
        return await self.repository.get_by_id(event_id)