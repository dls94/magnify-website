from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from application.exceptions import ArtistNotFoundError
from application.ports.artist_repository import ArtistRepositoryPort
from application.ports.user_repository import UserRepositoryPort
from application.use_cases.user.create_user import CreateUser
from domain.models.artist import Artist
from domain.models.user import User, UserRole
from tests.fakes.user_repository import InMemoryUserRepository


async def test_create_user():
    repository = InMemoryUserRepository()
    artist_repository = AsyncMock(spec=ArtistRepositoryPort)

    use_case = CreateUser(repository, artist_repository)

    user = await use_case.execute(
        email="admin@magnify.music",
        password_hash="hashed-password",
    )

    assert user.email == "admin@magnify.music"
    assert user.password_hash == "hashed-password"
    assert user.role == UserRole.ADMIN
    assert user.id in repository.users

async def test_create_artist_user_with_artist_id():
    repository = InMemoryUserRepository()
    artist_repository = AsyncMock(spec=ArtistRepositoryPort)

    artist_id = uuid4()
    artist_repository.get_by_id.return_value = Artist(
        name="Test Artist",
        id=artist_id,
    )

    use_case = CreateUser(repository, artist_repository)

    user = await use_case.execute(
        email="artist@magnify.music",
        password_hash="hashed-password",
        role=UserRole.ARTIST,
        artist_id=artist_id,
    )

    assert user.email == "artist@magnify.music"
    assert user.password_hash == "hashed-password"
    assert user.role == UserRole.ARTIST
    assert user.artist_id == artist_id
    assert user.id in repository.users

async def test_create_artist_user_rejects_unknown_artist():
    repository = AsyncMock(spec=UserRepositoryPort)
    artist_repository = AsyncMock(spec=ArtistRepositoryPort)

    artist_repository.get_by_id.return_value = None

    use_case = CreateUser(repository, artist_repository)

    with pytest.raises(ArtistNotFoundError, match="Artist not found"):
        await use_case.execute(
            email="artist@example.com",
            password_hash="hashed-password",
            role=UserRole.ARTIST,
            artist_id=uuid4(),
        )

    repository.save.assert_not_awaited()

async def test_create_artist_user_accepts_existing_artist():
    repository = AsyncMock(spec=UserRepositoryPort)
    artist_repository = AsyncMock(spec=ArtistRepositoryPort)

    artist_id = uuid4()
    artist_repository.get_by_id.return_value = Artist(
        name="Test Artist",
        id=artist_id,
    )

    user = User(
        email="artist@example.com",
        password_hash="hashed-password",
        role=UserRole.ARTIST,
        artist_id=artist_id,
    )
    repository.save.return_value = user

    use_case = CreateUser(repository, artist_repository)

    result = await use_case.execute(
        email="artist@example.com",
        password_hash="hashed-password",
        role=UserRole.ARTIST,
        artist_id=artist_id,
    )

    assert result.artist_id == artist_id
    repository.save.assert_awaited_once()