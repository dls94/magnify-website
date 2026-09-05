from typing import Protocol
from uuid import UUID

from domain.models.release import Release


class ReleaseRepositoryPort(Protocol):
    async def save(self, release: Release) -> Release:
        ...

    async def get_by_id(self, release_id: UUID) -> Release | None:
        ...

    async def list_all(self) -> list[Release]:
        ...

    async def delete(self, release_id: UUID) -> bool:
        ...