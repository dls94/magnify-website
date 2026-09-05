from uuid import UUID

from domain.models.event import Event


class InMemoryEventRepository:
    def __init__(self) -> None:
        self.events: dict[UUID, Event] = {}

    async def save(self, event: Event) -> Event:
        self.events[event.id] = event
        return event

    async def get_by_id(self, event_id: UUID) -> Event | None:
        return self.events.get(event_id)

    async def list_all(self) -> list[Event]:
        return list(self.events.values())

    async def list_upcoming(self) -> list[Event]:
        return [
            event
            for event in self.events.values()
            if not event.is_past()
        ]

    async def delete(self, event_id: UUID) -> bool:
        if event_id not in self.events:
            return False

        del self.events[event_id]
        return True