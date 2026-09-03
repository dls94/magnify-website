from dataclasses import dataclass, field
from datetime import datetime, date, timezone
from enum import Enum
from typing import Optional, List
from uuid import UUID, uuid4


class ReleaseType(str, Enum):
    SINGLE = "SINGLE"
    EP = "EP"
    ALBUM = "ALBUM"


@dataclass
class Track:
    title: str
    duration_seconds: int
    isrc: Optional[str] = None
    track_number: int = 1

    def __post_init__(self) -> None:
        if not self.title or not self.title.strip():
            raise ValueError("Le titre du morceau est obligatoire.")

        if self.duration_seconds <= 0:
            raise ValueError(
                "La durée du morceau doit être supérieure à zéro."
            )

        if self.track_number < 1:
            raise ValueError(
                "Le numéro de piste doit être supérieur ou égal à 1."
            )


@dataclass
class Release:

    title: str
    release_type: ReleaseType
    release_date: date
    cover_url: str | None
    id: UUID = field(default_factory=uuid4)
    artist_id: UUID | None = None
    cover_url: Optional[str] = None
    upc: Optional[str] = None  # Code barre produit / Universal Product Code
    spotify_url: Optional[str] = None
    tracks: List[Track] = field(default_factory=list)
    is_published: bool = False
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


    # 2. Règles Métier (Comportement de l'entité)
    def add_track(self, title: str, duration_seconds: int, isrc: Optional[str] = None) -> None:
        """Ajoute une piste à la sortie en incrémentant le numéro de piste."""
        track_number = len(self.tracks) + 1
        new_track = Track(
            title=title,
            duration_seconds=duration_seconds,
            isrc=isrc,
            track_number=track_number
        )
        self.tracks.append(new_track)

    def can_be_published(self) -> bool:
        """
        Règle métier : Une release ne peut être publiée sur le site que si :
        - Elle a au moins une piste (track).
        - Elle a une pochette (cover_url).
        """
        return bool(self.cover_url and len(self.tracks) > 0)

    def publish(self) -> None:
        """Publie la release si les conditions métier sont remplies."""

        if self.is_published:
            raise ValueError(
                "La release est déjà publiée."
            )

        if not self.can_be_published():
            raise ValueError(
                "Impossible de publier la release : il manque la pochette ou au moins un morceau."
            )
        self.is_published = True