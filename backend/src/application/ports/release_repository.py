# app/application/ports/release_repository.py
from abc import ABC, abstractmethod
from typing import Optional, List
from src.domain.models import Release


class ReleaseRepositoryPort(ABC):

    @abstractmethod
    def save(self, release: Release) -> Release:
        """Sauvegarde une sortie d'album/EP/Single."""
        pass

    @abstractmethod
    def get_by_id(self, release_id: str) -> Optional[Release]:
        """Récupère une sortie par son ID."""
        pass

    @abstractmethod
    def list_by_artist(self, artist_id: str) -> List[Release]:
        """Récupère toutes les sorties d'un artiste spécifique."""
        pass