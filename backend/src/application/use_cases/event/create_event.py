from datetime import datetime
from uuid import UUID

from application.ports.event_repository import EventRepositoryPort
from domain.models.event import Event, EventType


class CreateEvent:
    def __init__(self, repository: EventRepositoryPort) -> None:
        self.repository = repository

    async def execute(
        self,
        title: str,
        description: str,
        event_type: EventType,
        event_date: datetime,
        artist_id: UUID | None = None,
        venue_name: str | None = None,
        city: str | None = None,
        ticket_url: str | None = None,
        cover_image_url: str | None = None,
    ) -> Event:
        event = Event(
            title=title,
            description=description,
            event_type=event_type,
            event_date=event_date,
            artist_id=artist_id,
            venue_name=venue_name,
            city=city,
            ticket_url=ticket_url,
            cover_image_url=cover_image_url,
        )

        return await self.repository.save(event)