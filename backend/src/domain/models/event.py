from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from uuid import UUID, uuid4


class EventType(str, Enum):
    CONCERT = "CONCERT"
    FESTIVAL = "FESTIVAL"
    RELEASE_PARTY = "RELEASE_PARTY"
    NEWS = "NEWS"


@dataclass
class Event:

    title: str
    description: str
    event_type: EventType
    event_date: datetime
    id: UUID = field(default_factory=uuid4)
    artist_id: UUID | None = None
    venue_name: str | None = None
    city: str | None = None
    ticket_url: str | None = None
    cover_image_url: str | None = None
    is_published: bool = False
    created_at: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )

    def __post_init__(self) -> None:
        if not self.title or not self.title.strip():
            raise ValueError("Le titre de l'événement est obligatoire.")

        if self.event_date.tzinfo is None or self.event_date.utcoffset() is None:
            raise ValueError("La date doit être timezone-aware.")

    def is_past(self) -> bool:
        now = datetime.now(UTC)
        return self.event_date < now

    def publish(self) -> None:
        if self.is_published:
            raise ValueError("L'événement est déjà publié.")

        if not self.title or not self.title.strip() or not self.event_date:
            raise ValueError(
                "Impossible de publier un événement sans titre ni date."
            )

        self.is_published = True

    def update_profile(
            self,
            title: str | None = None,
            description: str | None = None,
            event_type: EventType | None = None,
            event_date: datetime | None = None,
            artist_id: UUID | None = None,
            venue_name: str | None = None,
            city: str | None = None,
            ticket_url: str | None = None,
            cover_image_url: str | None = None,
    ) -> None:
        if title is not None:
            if not title.strip():
                raise ValueError("Le titre de l'événement est obligatoire.")
            self.title = title

        if description is not None:
            self.description = description

        if event_type is not None:
            self.event_type = event_type

        if event_date is not None:
            if event_date.tzinfo is None or event_date.utcoffset() is None:
                raise ValueError("La date doit être timezone-aware.")
            self.event_date = event_date

        if artist_id is not None:
            self.artist_id = artist_id

        if venue_name is not None:
            self.venue_name = venue_name

        if city is not None:
            self.city = city

        if ticket_url is not None:
            self.ticket_url = ticket_url

        if cover_image_url is not None:
            self.cover_image_url = cover_image_url