from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Artist:

    id: Optional[str]
    name: str
    bio: Optional[str] = None
    spotify_url: Optional[str] = None
    instagram_url: Optional[str] = None
    picture_url: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)

    def update_social_links(self, spotify_url: Optional[str] = None, instagram_url: Optional[str] = None):
        """Exemple de règle métier : mise à jour des réseaux sociaux."""
        if spotify_url and not spotify_url.startswith("https://open.spotify.com/"):
            raise ValueError("L'URL Spotify est invalide.")

        if spotify_url:
            self.spotify_url = spotify_url
        if instagram_url:
            self.instagram_url = instagram_url

    def is_profile_complete(self) -> bool:
        """Vérifie si la fiche artiste est complète pour être affichée sur le site."""
        return bool(self.name and self.bio and self.picture_url)