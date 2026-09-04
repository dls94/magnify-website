from collections.abc import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.database.connection import AsyncSessionLocal
from application.ports.artist_repository import ArtistRepositoryPort
from infrastructure.database.repositories.artist_repository import ArtistRepository
from application.use_cases.artist.list_artists import ListArtists
from application.use_cases.artist.get_artist import GetArtist
from application.use_cases.artist.create_artist import CreateArtist
from application.use_cases.artist.update_artist import UpdateArtist
from application.use_cases.artist.delete_artist import DeleteArtist



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

def get_artist_use_case(
    repository: ArtistRepositoryPort = Depends(get_artist_repository),
) -> GetArtist:
    return GetArtist(repository)

def get_create_artist_use_case(
    repository: ArtistRepositoryPort = Depends(get_artist_repository),
) -> CreateArtist:
    return CreateArtist(repository)

def get_update_artist_use_case(
    repository: ArtistRepositoryPort = Depends(get_artist_repository),
) -> UpdateArtist:
    return UpdateArtist(repository)

def get_delete_artist_use_case(
    repository: ArtistRepositoryPort = Depends(get_artist_repository),
) -> DeleteArtist:
    return DeleteArtist(repository)