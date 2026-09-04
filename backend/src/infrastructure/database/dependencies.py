from collections.abc import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.database.connection import AsyncSessionLocal
from application.ports.artist_repository import ArtistRepositoryPort
from infrastructure.database.repositories.artist_repository import ArtistRepository
from application.use_cases.artist.list_artists import ListArtists




async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session

def get_artist_repository(
    session: AsyncSession = Depends(get_session),
) -> ArtistRepositoryPort:
    return ArtistRepository(session)

def get_list_artists_use_case(
    repository: ArtistRepositoryPort = Depends(get_artist_repository),
) -> ListArtists:
    return ListArtists(repository)