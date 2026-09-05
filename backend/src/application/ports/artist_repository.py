from typing import Protocol
from uuid import UUID

from domain.models import Artist


class ArtistRepositoryPort(Protocol):

    async def save(self, artist: Artist) -> Artist:
        pass

    async def get_by_id(self, artist_id: UUID) -> Artist | None:
        pass

    async def list_all(self) -> list[Artist]:
        pass

    async def delete(self, artist_id: UUID) -> bool:
        pass