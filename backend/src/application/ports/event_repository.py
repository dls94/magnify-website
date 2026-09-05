from typing import Protocol
from uuid import UUID

from domain.models.event import Event


class EventRepositoryPort(Protocol):
    async def save(self, event: Event) -> Event:
        """Sauvegarde un événement."""
        ...

    async def get_by_id(self, event_id: UUID) -> Event | None:
        """Récupère un événement par son ID."""
        ...

    async def list_all(self) -> list[Event]:
        """Récupère tous les événements."""
        ...

    async def list_upcoming(self) -> list[Event]:
        """Récupère les événements à venir."""
        ...

    async def delete(self, event_id: UUID) -> bool:
        """Supprime un événement."""
        ...