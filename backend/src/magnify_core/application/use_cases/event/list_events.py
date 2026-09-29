from magnify_core.application.ports.event_repository import EventRepositoryPort
from magnify_core.domain.models import Event


class ListEvents:
    def __init__(self, repository: EventRepositoryPort) -> None:
        self.repository = repository

    async def execute(self) -> list[Event]:
        return await self.repository.list_all()

    async def execute_upcoming(self) -> list[Event]:
        return await self.repository.list_upcoming()