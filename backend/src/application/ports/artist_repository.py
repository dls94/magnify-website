from abc import ABC, abstractmethod
from uuid import UUID
from domain.models import Artist


class ArtistRepositoryPort(ABC):

    @abstractmethod
    def save(self, artist: UUID) -> Artist | None:
        pass

    @abstractmethod
    def get_by_id(self, artist_id: UUID) -> Artist | None:
        pass

    @abstractmethod
    def list_all(self) -> list[Artist]:
        pass