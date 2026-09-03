from application.ports.artist_repository import ArtistRepositoryPort
from domain.models.artist import Artist


class CreateArtist:

    def __init__(self, repository: ArtistRepositoryPort) -> None:
        self.repository = repository

    def execute(
        self,
        name: str,
        bio: str | None = None,
        picture_url: str | None = None,
        spotify_url: str | None = None,
        instagram_url: str | None = None,
    ) -> Artist:
        artist = Artist(
            name=name,
            bio=bio,
            picture_url=picture_url,
            spotify_url=spotify_url,
            instagram_url=instagram_url,
        )

        return self.repository.save(artist)