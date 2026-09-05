from uuid import UUID

from domain.models.release import Release


class InMemoryReleaseRepository:
    def __init__(self) -> None:
        self.releases: dict[UUID, Release] = {}

    async def save(self, release: Release) -> Release:
        self.releases[release.id] = release
        return release

    async def get_by_id(self, release_id: UUID) -> Release | None:
        return self.releases.get(release_id)

    async def list_all(self) -> list[Release]:
        return list(self.releases.values())

    async def delete(self, release_id: UUID) -> bool:
        if release_id not in self.releases:
            return False

        del self.releases[release_id]
        return True