from uuid import UUID
from domain.models.artist import Artist


class InMemoryArtistRepository:

    def __init__(self) -> None:
        self.artists: dict[UUID, Artist] = {}

    async def save(self, artist: Artist) -> Artist:
        self.artists[artist.id] = artist
        return artist

    async def get_by_id(self, artist_id: UUID) -> Artist | None:
        return self.artists.get(artist_id)

    async def list_all(self) -> list[Artist]:
        return list(self.artists.values())

    async def delete(self, artist_id: UUID) -> bool:
        if artist_id not in self.artists:
            return False

        del self.artists[artist_id]
        return True