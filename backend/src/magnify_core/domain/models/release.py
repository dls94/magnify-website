from dataclasses import dataclass, field
from datetime import UTC, date, datetime
from enum import Enum
from uuid import UUID, uuid4


class ReleaseType(str, Enum):
    SINGLE = "SINGLE"
    EP = "EP"
    ALBUM = "ALBUM"


@dataclass
class Track:
    title: str
    duration_seconds: int
    isrc: str | None = None
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
    id: UUID = field(default_factory=uuid4)
    cover_url: str | None = None
    artist_id: UUID | None = None
    upc: str | None = None  # Code barre produit / Universal Product Code
    spotify_url: str | None = None
    tracks: list[Track] = field(default_factory=list)
    is_published: bool = False
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))


    # 2. Règles Métier (Comportement de l'entité)
    def add_track(self, title: str, duration_seconds: int, isrc: str | None = None) -> None:
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

    def update_profile(
            self,
            title: str | None = None,
            release_type: ReleaseType | None = None,
            release_date: date | None = None,
            cover_url: str | None = None,
            upc: str | None = None,
            spotify_url: str | None = None,
            artist_id: UUID | None = None,
            artist_id_provided: bool = False,
    ) -> None:
        if title is not None:
            if not title.strip():
                raise ValueError("Le titre de la release est obligatoire.")
            self.title = title

        if release_type is not None:
            self.release_type = release_type

        if release_date is not None:
            self.release_date = release_date

        if cover_url is not None:
            self.cover_url = cover_url

        if upc is not None:
            self.upc = upc

        if spotify_url is not None:
            self.spotify_url = spotify_url

        if artist_id_provided:
            self.artist_id = artist_id