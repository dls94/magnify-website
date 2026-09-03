from abc import ABC, abstractmethod
from uuid import UUID

from domain.models.event import Event


class EventRepositoryPort(ABC):

    @abstractmethod
    def save(self, event: Event) -> Event:
        """Sauvegarde un événement."""
        ...

    @abstractmethod
    def get_by_id(self, event_id: UUID) -> Event | None:
        """Récupère un événement par son ID."""
        ...

    @abstractmethod
    def list_all(self) -> list[Event]:
        """Récupère tous les événements."""
        ...

    @abstractmethod
    def list_upcoming(self) -> list[Event]:
        """Récupère les événements à venir."""
        ...