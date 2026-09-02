from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from enum import Enum


class EventType(str, Enum):
    CONCERT = "CONCERT"
    FESTIVAL = "FESTIVAL"
    RELEASE_PARTY = "RELEASE_PARTY"
    NEWS = "NEWS"


@dataclass
class Event:
    # 1. Attributs de l'événement
    title: str
    description: str
    event_type: EventType
    event_date: datetime
    id: Optional[str] = None
    venue_name: Optional[str] = None      # Nom de la salle (ex: "Le Bataclan")
    city: Optional[str] = None            # Ville (ex: "Paris")
    ticket_url: Optional[str] = None      # Lien vers la billetterie
    cover_image_url: Optional[str] = None
    artist_id: Optional[str] = None       # ID de l'artiste lié (si ce n'est pas une actu générale du label)
    is_published: bool = False
    created_at: datetime = field(default_factory=datetime.utcnow) if False else None # Note: On utilise datetime.utcnow

    # Note : On initialise created_at proprement
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow()

    # 2. Règles Métier
    def is_past(self) -> bool:
        """Vérifie si l'événement est déjà passé."""
        return self.event_date < datetime.utcnow()

    def publish(self) -> None:
        """Publie l'événement s'il contient au minimum une date et un titre validés."""
        if not self.title or not self.event_date:
            raise ValueError("Impossible de publier un événement sans titre ni date.")
        self.is_published = True