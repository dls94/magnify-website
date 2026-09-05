from uuid import UUID

from application.ports.event_repository import EventRepositoryPort
from domain.models.event import Event


class GetEvent:
    def __init__(self, repository: EventRepositoryPort) -> None:
        self.repository = repository

    async def execute(self, event_id: UUID) -> Event | None:
        return await self.repository.get_by_id(event_id)