from typing import Protocol
from uuid import UUID
from domain.models import Artist


class ArtistRepositoryPort(Protocol):

    def save(self, artist: Artist) -> Artist:
        pass

    def get_by_id(self, artist_id: UUID) -> Artist | None:
        pass

    def list_all(self) -> list[Artist]:
        pass