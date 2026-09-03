from abc import ABC, abstractmethod
from uuid import UUID

from domain.models import Release


class ReleaseRepositoryPort(ABC):

    @abstractmethod
    def save(self, release: Release) -> Release:
        """Sauvegarde une sortie d'album/EP/Single."""
        pass

    @abstractmethod
    def get_by_id(self, release_id: UUID) -> Release | None:
        """Récupère une sortie par son ID."""
        pass

    @abstractmethod
    def list_by_artist(self, artist_id: UUID) -> list[Release]:
        """Récupère toutes les sorties d'un artiste spécifique."""
        pass