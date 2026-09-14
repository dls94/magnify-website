from datetime import datetime
from uuid import UUID

from application.exceptions import ArtistNotFoundError
from application.ports.artist_repository import ArtistRepositoryPort
from application.ports.event_repository import EventRepositoryPort
from domain.models.event import Event, EventType


class CreateEvent:
    def __init__(
        self,
        repository: EventRepositoryPort,
        artist_repository: ArtistRepositoryPort,
    ) -> None:
        self.repository = repository
        self.artist_repository = artist_repository

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
        if artist_id is not None:
            artist = await self.artist_repository.get_by_id(artist_id)

            if artist is None:
                raise ArtistNotFoundError("Artist not found")

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