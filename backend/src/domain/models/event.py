from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Optional
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
    venue_name: Optional[str] = None
    city: Optional[str] = None
    ticket_url: Optional[str] = None
    cover_image_url: Optional[str] = None
    is_published: bool = False
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    def __post_init__(self) -> None:
        if not self.title or not self.title.strip():
            raise ValueError("Le titre de l'événement est obligatoire.")

    def is_past(self) -> bool:
        now = datetime.now(timezone.utc)
        return self.event_date < now

    def publish(self) -> None:
        if self.is_published:
            raise ValueError("L'événement est déjà publié.")

        if not self.title or not self.title.strip() or not self.event_date:
            raise ValueError(
                "Impossible de publier un événement sans titre ni date."
            )

        self.is_published = True