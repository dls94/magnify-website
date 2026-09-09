from collections.abc import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from application.ports.artist_repository import ArtistRepositoryPort
from application.ports.event_repository import EventRepositoryPort
from application.ports.release_repository import ReleaseRepositoryPort
from application.ports.user_repository import UserRepositoryPort
from application.use_cases.artist.create_artist import CreateArtist
from application.use_cases.artist.delete_artist import DeleteArtist
from application.use_cases.artist.get_artist import GetArtist
from application.use_cases.artist.get_current_artist import GetCurrentArtist
from application.use_cases.artist.list_artists import ListArtists
from application.use_cases.artist.update_artist import UpdateArtist
from application.use_cases.event.create_event import CreateEvent
from application.use_cases.event.delete_event import DeleteEvent
from application.use_cases.event.get_event import GetEvent
from application.use_cases.event.list_events import ListEvents
from application.use_cases.event.update_event import UpdateEvent
from application.use_cases.release.create_release import CreateRelease
from application.use_cases.release.delete_release import DeleteRelease
from application.use_cases.release.get_current_artist_releases import (
    GetCurrentArtistReleases,
)
from application.use_cases.release.get_release import GetRelease
from application.use_cases.release.list_releases import ListReleases
from application.use_cases.release.update_release import UpdateRelease
from application.use_cases.user.authenticate_user import AuthenticateUser
from application.use_cases.user.create_user import CreateUser
from application.use_cases.user.delete_user import DeleteUser
from application.use_cases.user.get_user import GetUser
from application.use_cases.user.list_users import ListUsers
from application.use_cases.user.update_user import UpdateUser
from infrastructure.config import Settings
from infrastructure.database.connection import AsyncSessionLocal
from infrastructure.database.repositories.artist_repository import ArtistRepository
from infrastructure.database.repositories.event_repository import EventRepository
from infrastructure.database.repositories.release_repository import ReleaseRepository
from infrastructure.database.repositories.user_repository import UserRepository
from infrastructure.security.argon2_password_hasher import Argon2PasswordHasher
from infrastructure.security.jwt_token_provider import JwtTokenProvider


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
    artist_repository: ArtistRepositoryPort = Depends(get_artist_repository),
) -> CreateRelease:
    return CreateRelease(repository, artist_repository)

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

def get_event_repository(
    session: AsyncSession = Depends(get_session),
) -> EventRepositoryPort:
    return EventRepository(session)

def get_create_event_use_case(
    repository: EventRepositoryPort = Depends(get_event_repository),
) -> CreateEvent:
    return CreateEvent(repository)


def get_event_use_case(
    repository: EventRepositoryPort = Depends(get_event_repository),
) -> GetEvent:
    return GetEvent(repository)


def get_list_events_use_case(
    repository: EventRepositoryPort = Depends(get_event_repository),
) -> ListEvents:
    return ListEvents(repository)


def get_update_event_use_case(
    repository: EventRepositoryPort = Depends(get_event_repository),
) -> UpdateEvent:
    return UpdateEvent(repository)


def get_delete_event_use_case(
    repository: EventRepositoryPort = Depends(get_event_repository),
) -> DeleteEvent:
    return DeleteEvent(repository)

def get_token_provider() -> JwtTokenProvider:
    settings = Settings()

    return JwtTokenProvider(
        secret_key=settings.jwt_secret_key,
        access_token_expire_minutes=settings.access_token_expire_minutes,
    )

def get_user_repository(
    session: AsyncSession = Depends(get_session),
) -> UserRepositoryPort:
    return UserRepository(session)

def get_authenticate_user(
    repository: UserRepositoryPort = Depends(get_user_repository),
) -> AuthenticateUser:
    password_hasher = Argon2PasswordHasher()

    return AuthenticateUser(
        repository=repository,
        password_hasher=password_hasher,
    )

def get_create_user_use_case(
    repository: UserRepositoryPort = Depends(get_user_repository),
) -> CreateUser:
    return CreateUser(repository)

def get_password_hasher() -> Argon2PasswordHasher:
    return Argon2PasswordHasher()

def get_list_users_use_case(
    repository: UserRepositoryPort = Depends(get_user_repository),
) -> ListUsers:
    return ListUsers(repository)

def get_get_user_use_case(
    repository: UserRepositoryPort = Depends(get_user_repository),
) -> GetUser:
    return GetUser(repository)

def get_update_user_use_case(
    repository: UserRepositoryPort = Depends(get_user_repository),
) -> UpdateUser:
    return UpdateUser(repository)

def get_delete_user_use_case(
    repository: UserRepositoryPort = Depends(get_user_repository),
) -> DeleteUser:
    return DeleteUser(repository)

def get_current_artist_use_case(
    repository: ArtistRepositoryPort = Depends(get_artist_repository),
) -> GetCurrentArtist:
    return GetCurrentArtist(repository)

def get_current_artist_releases_use_case(
    repository: ReleaseRepositoryPort = Depends(get_release_repository),
) -> GetCurrentArtistReleases:
    return GetCurrentArtistReleases(repository)