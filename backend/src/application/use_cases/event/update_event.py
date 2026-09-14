from datetime import datetime
from uuid import UUID

from application.exceptions import ArtistNotFoundError
from application.ports.artist_repository import ArtistRepositoryPort
from application.ports.event_repository import EventRepositoryPort
from domain.models.event import Event, EventType


class UpdateEvent:
    def __init__(
        self,
        repository: EventRepositoryPort,
        artist_repository: ArtistRepositoryPort,
    ) -> None:
        self.repository = repository
        self.artist_repository = artist_repository

    async def execute(
        self,
        event_id: UUID,
        title: str | None = None,
        description: str | None = None,
        event_type: EventType | None = None,
        event_date: datetime | None = None,
        artist_id: UUID | None = None,
        artist_id_provided: bool = False,
        venue_name: str | None = None,
        city: str | None = None,
        ticket_url: str | None = None,
        cover_image_url: str | None = None,
    ) -> Event | None:
        event = await self.repository.get_by_id(event_id)

        if event is None:
            return None

        if artist_id_provided and artist_id is not None:
            artist = await self.artist_repository.get_by_id(artist_id)

            if artist is None:
                raise ArtistNotFoundError("Artist not found")

        event.update_profile(
            title=title,
            description=description,
            event_type=event_type,
            event_date=event_date,
            artist_id=artist_id,
            artist_id_provided=artist_id_provided,
            venue_name=venue_name,
            city=city,
            ticket_url=ticket_url,
            cover_image_url=cover_image_url,
        )

        return await self.repository.save(event)