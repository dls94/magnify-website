from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.models import Artist


class ArtistRepositoryPort(ABC):

    @abstractmethod
    def save(self, artist: Artist) -> Artist:
        pass

    @abstractmethod
    def get_by_id(self, artist_id: int) -> Optional[Artist]:
        pass

    @abstractmethod
    def list_all(self) -> List[Artist]:
        pass