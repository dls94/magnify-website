from application.ports.artist_repository import ArtistRepositoryPort
from domain.models.artist import Artist


class ListArtists:

    def __init__(self, repository: ArtistRepositoryPort) -> None:
        self.repository = repository

    def execute(self) -> list[Artist]:
        return self.repository.list_all()