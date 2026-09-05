from uuid import UUID

from application.ports.event_repository import EventRepositoryPort


class DeleteEvent:
    def __init__(self, repository: EventRepositoryPort) -> None:
        self.repository = repository

    async def execute(self, event_id: UUID) -> bool:
        return await self.repository.delete(event_id)