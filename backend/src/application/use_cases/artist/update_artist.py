from uuid import UUID

from application.ports.artist_repository import ArtistRepositoryPort
from domain.models.artist import Artist


class UpdateArtist:
    def __init__(self, repository: ArtistRepositoryPort) -> None:
        self.repository = repository

    def execute(
        self,
        artist_id: UUID,
        name: str | None = None,
        bio: str | None = None,
        picture_url: str | None = None,
        spotify_url: str | None = None,
        instagram_url: str | None = None,
    ) -> Artist | None:
        artist = self.repository.get_by_id(artist_id)

        if artist is None:
            return None

        artist.update_profile(
            name=name,
            bio=bio,
            picture_url=picture_url,
            spotify_url=spotify_url,
            instagram_url=instagram_url,
        )

        return self.repository.save(artist)