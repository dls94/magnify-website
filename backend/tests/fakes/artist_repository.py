from uuid import UUID

from application.ports.artist_repository import ArtistRepositoryPort
from domain.models.artist import Artist


class InMemoryArtistRepository(ArtistRepositoryPort):

    def __init__(self) -> None:
        self.artists: dict[UUID, Artist] = {}

    def save(self, artist: Artist) -> Artist:
        self.artists[artist.id] = artist
        return artist

    def get_by_id(self, artist_id: UUID) -> Artist | None:
        return self.artists.get(artist_id)

    def list_all(self) -> list[Artist]:
        return list(self.artists.values())