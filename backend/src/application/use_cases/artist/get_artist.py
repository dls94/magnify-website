from uuid import UUID

from domain.models.artist import Artist
from application.ports.artist_repository import ArtistRepositoryPort


class GetArtist:

    def __init__(self, repository: ArtistRepositoryPort) -> None:
        self.repository = repository

    def execute(self, artist_id: UUID) -> Artist | None:
        return self.repository.get_by_id(artist_id)