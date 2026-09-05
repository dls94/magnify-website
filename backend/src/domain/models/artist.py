from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID, uuid4


@dataclass
class Artist:

    name: str
    id: UUID = field(default_factory=uuid4)
    bio: str | None = None
    spotify_url: str | None = None
    instagram_url: str | None = None
    picture_url: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def __post_init__(self) -> None:
        if not self.name or not self.name.strip():
            raise ValueError("Le nom de l'artiste est obligatoire.")

    def update_social_links(
            self,
            spotify_url: str | None = None,
            instagram_url: str | None = None
    ) -> None:
        """Exemple de règle métier : mise à jour des réseaux sociaux."""

        if spotify_url and not spotify_url.startswith("https://open.spotify.com/"):
            raise ValueError("L'URL Spotify est invalide.")

        if spotify_url:
            self.spotify_url = spotify_url
        if instagram_url:
            self.instagram_url = instagram_url

    def is_profile_complete(self) -> bool:
        """Vérifie si la fiche artiste est complète pour être affichée sur le site."""
        return bool(
            self.name
            and self.bio
            and self.picture_url
        )

    def update_profile(
            self,
            name: str | None = None,
            bio: str | None = None,
            picture_url: str | None = None,
            spotify_url: str | None = None,
            instagram_url: str | None = None,
    ) -> None:
        if name is not None:
            if not name.strip():
                raise ValueError("Le nom de l'artiste est obligatoire.")
            self.name = name

        if bio is not None:
            self.bio = bio

        if picture_url is not None:
            self.picture_url = picture_url

        if spotify_url is not None:
            if not spotify_url.startswith("https://open.spotify.com/"):
                raise ValueError("L'URL Spotify est invalide.")
            self.spotify_url = spotify_url

        if instagram_url is not None:
            self.instagram_url = instagram_url