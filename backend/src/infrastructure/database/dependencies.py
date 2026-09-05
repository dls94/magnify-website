from collections.abc import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from application.ports.artist_repository import ArtistRepositoryPort
from application.ports.release_repository import ReleaseRepositoryPort
from application.use_cases.artist.create_artist import CreateArtist
from application.use_cases.artist.delete_artist import DeleteArtist
from application.use_cases.artist.get_artist import GetArtist
from application.use_cases.artist.list_artists import ListArtists
from application.use_cases.artist.update_artist import UpdateArtist
from application.use_cases.release.create_release import CreateRelease
from application.use_cases.release.delete_release import DeleteRelease
from application.use_cases.release.get_release import GetRelease
from application.use_cases.release.list_releases import ListReleases
from application.use_cases.release.update_release import UpdateRelease
from infrastructure.database.connection import AsyncSessionLocal
from infrastructure.database.repositories.artist_repository import ArtistRepository
from infrastructure.database.repositories.release_repository import ReleaseRepository


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

def get_release_repository(
    session: AsyncSession = Depends(get_session),
) -> ReleaseRepositoryPort:
    return ReleaseRepository(session)


def get_create_release_use_case(
    repository: ReleaseRepositoryPort = Depends(get_release_repository),
) -> CreateRelease:
    return CreateRelease(repository)

def get_release_use_case(
    repository: ReleaseRepositoryPort = Depends(get_release_repository),
) -> GetRelease:
    return GetRelease(repository)

def get_list_releases_use_case(
    repository: ReleaseRepositoryPort = Depends(get_release_repository),
) -> ListReleases:
    return ListReleases(repository)

def get_update_release_use_case(
    repository: ReleaseRepositoryPort = Depends(get_release_repository),
) -> UpdateRelease:
    return UpdateRelease(repository)

def get_delete_release_use_case(
    repository: ReleaseRepositoryPort = Depends(get_release_repository),
) -> DeleteRelease:
    return DeleteRelease(repository)